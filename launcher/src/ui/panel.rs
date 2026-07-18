//--------------------------------

// Imports
use std::{num::NonZeroU32, rc::Rc};

use softbuffer::Surface;
use winit::window::Window;
use font8x8::{UnicodeFonts, BASIC_FONTS};

use crate::colors::rgba;
use crate::colors::blending_to_rgba;
//--------------------------------


fn draw_x_button(buffer: &mut [u32], width: u32, cx: u32, cy: u32) {
    let color = rgba(200, 200, 200, 125);
    let half = 7;

    for i in 0..=(half * 2) {
        //: \\
        let x = cx - half + i;
        let y = cy - half + i;
        buffer[(y * width + x+1) as usize] = color;
        buffer[(y * width + x) as usize] = color;

        //: //
        let x = cx + half - i;
        let y = cy - half + i;
        buffer[(y * width + x+1) as usize] = color;
        buffer[(y * width + x) as usize] = color;
    }
}


fn draw_text(buffer: &mut [u32], width: u32, text: &str, start_x: u32, start_y: u32, color: u32, scale:u32) {
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

                                buffer[((y + sy as u32) * width + (x + sx as u32)) as usize] = color;
                            }
                        }
                    }
                }
            }
        }

        cursor_x += 7 * scale;
    }
}


fn draw_status_box(buffer: &mut [u32], width: u32, x: u32, y: u32, rectangle_width: u32, rectangle_height: u32, color: u32) {
    for row in y..y + rectangle_height {
        for column in x..x + rectangle_width {
            let index = (row * width + column) as usize;
            buffer[index] = color;
        }
    }
}
//--------------------------------


pub fn draw_panel(window: &Window, surface: &mut Surface<Rc<Window>, Rc<Window>>) {
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
            buffer[(y * width + x) as usize] = blending_to_rgba(0.5, 0.25, 128);
        }
    }
    draw_x_button(&mut buffer, width, 18, 18);
    
    let status_x = 20;
    let status_y = 40;
    let status_button_text = "Status";
    let status_len = status_button_text.len() as u32;
    let status_scale = 2;

    draw_text(
        &mut buffer,
        width,
        status_button_text,
        status_x,
        status_y,
        rgba(255, 255, 255, 255),
        status_scale
    );

    draw_status_box(
        &mut buffer,
        width,
        status_x + status_len * status_scale * 8,
        status_y - 20 + (4*status_scale),
        40,
        40,
        rgba(200, 50, 50, 255),
    );

    buffer.present().unwrap();
}
//--------------------------------

