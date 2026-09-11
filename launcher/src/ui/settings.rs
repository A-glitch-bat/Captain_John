//--------------------------------

// Imports
use std::cmp;

use font8x8::{BASIC_FONTS, UnicodeFonts};

use crate::colors::{blending_to_rgba, rgba};
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
        Self {
            x,
            y,
            width,
            height,
        }
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

fn draw_text(
    buffer: &mut [u32],
    width: u32,
    height: u32,
    text: &str,
    start_x: u32,
    start_y: u32,
    color: u32,
) {
    let mut cursor_x = start_x;

    for character in text.chars() {
        if let Some(glyph) = BASIC_FONTS.get(character) {
            for (row, bits) in glyph.iter().enumerate() {
                for column in 0..8 {
                    if bits & (1 << column) != 0 {
                        put_pixel(
                            buffer,
                            width,
                            height,
                            cursor_x + column,
                            start_y + row as u32,
                            color,
                        );
                    }
                }
            }
        }

        cursor_x += 7;
    }
}

fn draw_setting_row(
    buffer: &mut [u32],
    width: u32,
    height: u32,
    rect: Rect,
    label: &str,
    value: &str,
) {
    draw_rect(buffer, width, height, rect, rgba(8, 10, 18, 205));
    draw_frame(buffer, width, height, rect, rgba(0, 255, 255, 75));
    draw_text(
        buffer,
        width,
        height,
        label,
        rect.x + 8,
        rect.y + 8,
        rgba(255, 210, 235, 230),
    );
    draw_text(
        buffer,
        width,
        height,
        value,
        rect.x + rect.width.saturating_sub(40),
        rect.y + 8,
        rgba(0, 255, 255, 220),
    );
}

pub fn draw_settings_popover(
    buffer: &mut [u32],
    width: u32,
    height: u32,
    x: u32,
    y: u32,
    popover_width: u32,
    popover_height: u32,
) {
    let rect = Rect::new(x, y, popover_width, popover_height);
    let stem = Rect::new(
        x + popover_width.saturating_sub(34),
        y.saturating_sub(5),
        18,
        6,
    );

    draw_rect(buffer, width, height, stem, rgba(12, 14, 25, 235));
    draw_rect(buffer, width, height, rect, rgba(10, 12, 22, 235));
    draw_frame(buffer, width, height, rect, rgba(255, 105, 180, 180));
    draw_frame(
        buffer,
        width,
        height,
        Rect::new(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4),
        rgba(0, 255, 255, 80),
    );

    draw_rect(
        buffer,
        width,
        height,
        Rect::new(rect.x + 3, rect.y + 3, rect.width - 6, 20),
        blending_to_rgba(0.16, 0.18, 210),
    );
    draw_text(
        buffer,
        width,
        height,
        "SETTINGS",
        rect.x + 10,
        rect.y + 9,
        rgba(255, 245, 255, 245),
    );

    draw_setting_row(
        buffer,
        width,
        height,
        Rect::new(rect.x + 8, rect.y + 31, rect.width - 16, 19),
        "AUTO FRONT",
        "OFF",
    );
    draw_setting_row(
        buffer,
        width,
        height,
        Rect::new(rect.x + 8, rect.y + 55, rect.width - 16, 19),
        "AUTO BACK",
        "ON",
    );
    draw_setting_row(
        buffer,
        width,
        height,
        Rect::new(rect.x + 8, rect.y + 79, rect.width - 16, 19),
        "PIN PANEL",
        "ON",
    );
}
//--------------------------------
