//--------------------------------

// Imports
use std::{cmp, num::NonZeroU32, rc::Rc};

use softbuffer::Surface;
use winit::window::Window;
use font8x8::{UnicodeFonts, BASIC_FONTS};

use crate::colors::{rgba, blending_to_rgba, lighten, darken};
use crate::status::Status;
//--------------------------------


#[derive(Clone, Copy)]
struct Rect {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
}

impl Rect {
    const fn new(x: u32, y: u32, width: u32, height: u32) -> Self {
        Self { x, y, width, height }
    }
}

fn put_pixel(buffer: &mut [u32], width: u32, height: u32, x: u32, y: u32, color: u32) {
    if x < width && y < height {
        buffer[(y * width + x) as usize] = color;
    }
}

fn draw_rect(buffer: &mut [u32], width: u32, height: u32, rect: Rect, color: u32) {
    let right = cmp::min(rect.x + rect.width, width);
    let bottom = cmp::min(rect.y + rect.height, height);

    for y in rect.y..bottom {
        for x in rect.x..right {
            put_pixel(buffer, width, height, x, y, color);
        }
    }
}

fn draw_frame(buffer: &mut [u32], width: u32, height: u32, rect: Rect, color: u32) {
    if rect.width < 2 || rect.height < 2 {
        return;
    }

    let right = rect.x + rect.width - 1;
    let bottom = rect.y + rect.height - 1;

    for x in rect.x..=right {
        put_pixel(buffer, width, height, x, rect.y, color);
        put_pixel(buffer, width, height, x, bottom, color);
    }

    for y in rect.y..=bottom {
        put_pixel(buffer, width, height, rect.x, y, color);
        put_pixel(buffer, width, height, right, y, color);
    }
}

fn draw_x_button(buffer: &mut [u32], width: u32, height: u32, cx: u32, cy: u32) {
    let frame = Rect::new(6, 6, 26, 26);
    let color = rgba(220, 220, 220, 190);
    let half = 6;

    draw_frame(buffer, width, height, frame, rgba(255, 105, 180, 140));
    draw_frame(
        buffer,
        width,
        height,
        Rect::new(frame.x + 2, frame.y + 2, frame.width - 4, frame.height - 4),
        rgba(255, 255, 255, 45),
    );

    for i in 0..=(half * 2) {
        //: \\
        let x = cx - half + i;
        let y = cy - half + i;
        put_pixel(buffer, width, height, x + 1, y, color);
        put_pixel(buffer, width, height, x, y, color);

        //: //
        let x = cx + half - i;
        let y = cy - half + i;
        put_pixel(buffer, width, height, x + 1, y, color);
        put_pixel(buffer, width, height, x, y, color);
    }
}


fn text_width(text: &str, scale: u32) -> u32 {
    text.chars().count() as u32 * 7 * scale
}


fn draw_text(buffer: &mut [u32], width: u32, height: u32, text: &str, start_x: u32, start_y: u32, color: u32, scale:u32) {
    let mut cursor_x = start_x;

    for character in text.chars() {
        if let Some(glyph) = BASIC_FONTS.get(character) {

            for (row, bits) in glyph.iter().enumerate() {

                for column in 0..8 {

                    if bits & (1 << column) != 0 {

                        let x = cursor_x + column * scale;
                        let y = start_y + row as u32 * scale;

                        for sy in 0..scale {
                            for sx in 0..scale {

                                put_pixel(buffer, width, height, x + sx, y + sy, color);
                            }
                        }
                    }
                }
            }
        }

        cursor_x += 7 * scale;
    }
}


fn draw_centered_text(buffer: &mut [u32], width: u32, height: u32, rect: Rect, text: &str, color: u32, scale:u32) {
    let x = rect.x + rect.width.saturating_sub(text_width(text, scale)) / 2;
    let y = rect.y + rect.height.saturating_sub(8 * scale) / 2;

    draw_text(buffer, width, height, text, x, y, color, scale);
}


fn status_label(status: &Status) -> &'static str {
    match status {
        Status::Offline => "OFFLINE",
        Status::Starting => "STARTING",
        Status::Online => "ONLINE",
    }
}


fn draw_button(buffer: &mut [u32], width: u32, height: u32, rect: Rect, label: &str, active: bool) {
    let fill = if active {
        blending_to_rgba(0.0, 0.22, 215)
    } else {
        rgba(18, 20, 30, 210)
    };
    let border = if active {
        rgba(0, 255, 255, 230)
    } else {
        rgba(255, 105, 180, 170)
    };
    let text = if active {
        rgba(0, 255, 255, 255)
    } else {
        rgba(255, 210, 235, 245)
    };

    draw_rect(buffer, width, height, rect, fill);
    draw_frame(buffer, width, height, rect, border);
    draw_frame(
        buffer,
        width,
        height,
        Rect::new(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4),
        rgba(255, 255, 255, 35),
    );
    draw_centered_text(buffer, width, height, rect, label, text, 1);
}


fn draw_status_box(buffer: &mut [u32], width: u32, height: u32, x: u32, y: u32, rectangle_width: u32, rectangle_height: u32, color: u32) {
    draw_rect(buffer, width, height, Rect::new(x, y, rectangle_width, rectangle_height), color);

    // highlight the edge of the border
    let highlight_color = lighten(color, 50, 255);
    for column in x..x + rectangle_width {
        put_pixel(buffer, width, height, column, y + 2, highlight_color);
        put_pixel(buffer, width, height, column, y + rectangle_height - 3, highlight_color);
    }
    for row in y..y + rectangle_height {
        put_pixel(buffer, width, height, x + 2, row, highlight_color);
        put_pixel(buffer, width, height, x - 3 + rectangle_width, row, highlight_color);
    }

    // darken 2 border pixels
    let border_color = darken(color, 50, 255);
    for column in x..x + rectangle_width {
        put_pixel(buffer, width, height, column, y, border_color);
        put_pixel(buffer, width, height, column, y + 1, border_color);
        put_pixel(buffer, width, height, column, y + rectangle_height - 2, border_color);
        put_pixel(buffer, width, height, column, y + rectangle_height - 1, border_color);
    }
    for row in y..y + rectangle_height {
        put_pixel(buffer, width, height, x, row, border_color);
        put_pixel(buffer, width, height, x + 1, row, border_color);
        put_pixel(buffer, width, height, x - 2 + rectangle_width, row, border_color);
        put_pixel(buffer, width, height, x - 1 + rectangle_width, row, border_color);
    }

}


fn draw_console_row(buffer: &mut [u32], width: u32, height: u32, y: u32, label: &str, value: &str) {
    let row = Rect::new(16, y, width.saturating_sub(88), 32);

    draw_rect(buffer, width, height, row, rgba(8, 10, 18, 170));
    draw_frame(buffer, width, height, row, rgba(0, 255, 255, 85));
    draw_text(buffer, width, height, label, row.x + 10, row.y + 12, rgba(255, 210, 235, 235), 1);
    draw_text(buffer, width, height, value, row.x + 142, row.y + 12, rgba(150, 170, 180, 200), 1);
}
//--------------------------------


pub fn draw_panel(
    window: &Window, 
    surface: &mut Surface<Rc<Window>, Rc<Window>>,
    status: &Status
) {
    let size = window.inner_size();

    surface
        .resize(
            NonZeroU32::new(size.width).unwrap(),
            NonZeroU32::new(size.height).unwrap(),
        )
        .unwrap();

    let mut buffer: softbuffer::Buffer<'_, Rc<Window>, Rc<Window>> = surface.buffer_mut().unwrap();

    let width = size.width;
    let height = size.height;

    for y in 0..height {
        for x in 0..width {
            buffer[(y * width + x) as usize] = rgba(4, 6, 12, 215);
        }
    }

    draw_frame(
        &mut buffer,
        width,
        height,
        Rect::new(0, 0, width, height),
        blending_to_rgba(0.82, 0.8, 180),
    );
    draw_rect(
        &mut buffer,
        width,
        height,
        Rect::new(0, 0, width, 48),
        blending_to_rgba(0.16, 0.18, 190),
    );
    draw_frame(
        &mut buffer,
        width,
        height,
        Rect::new(2, 2, width.saturating_sub(4), height.saturating_sub(4)),
        rgba(255, 105, 180, 65),
    );

    draw_x_button(&mut buffer, width, height, 18, 18);
    draw_text(
        &mut buffer,
        width,
        height,
        "CAPTAIN JOHN",
        44,
        14,
        rgba(255, 245, 255, 255),
        1
    );
    draw_text(
        &mut buffer,
        width,
        height,
        "LAUNCHER",
        44,
        27,
        rgba(0, 255, 255, 220),
        1
    );
    
    let indicator_x = width.saturating_sub(56);
    let indicator_y = 58;

    draw_console_row(
        &mut buffer,
        width,
        height,
        62,
        "FRONTEND",
        status_label(status),
    );

    draw_text(
        &mut buffer,
        width,
        height,
        "POWER",
        indicator_x,
        indicator_y + 44,
        rgba(0, 255, 255, 180),
        1
    );

    draw_status_box(
        &mut buffer,
        width,
        height,
        indicator_x,
        indicator_y,
        40,
        40,
        status.color()
    );

    draw_console_row(
        &mut buffer,
        width,
        height,
        106,
        "BACKEND",
        "STANDBY",
    );

    draw_button(
        &mut buffer,
        width,
        height,
        Rect::new(16, 158, width.saturating_sub(32), 34),
        "CYBERSPACE",
        false,
    );

    buffer.present().unwrap();
}
//--------------------------------
