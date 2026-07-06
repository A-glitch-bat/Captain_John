//--------------------------------

// Imports
use std::{num::NonZeroU32, rc::Rc};

use softbuffer::Surface;
use winit::window::Window;
//--------------------------------

use crate::colors::rgba;
use crate::colors::blending_to_rgba;

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

pub fn draw_panel(window: &Window, surface: &mut Surface<Rc<Window>, Rc<Window>>) {
    let size = window.inner_size();

    surface
        .resize(
            NonZeroU32::new(size.width).unwrap(),
            NonZeroU32::new(size.height).unwrap(),
        )
        .unwrap();

    let mut buffer = surface.buffer_mut().unwrap();

    let width = size.width;
    let height = size.height;

    for y in 0..height {
        for x in 0..width {
            buffer[(y * width + x) as usize] = blending_to_rgba(0.5, 0.25, 128);
        }
    }
    draw_x_button(&mut buffer, width, 18, 18);

    buffer.present().unwrap();
}
//--------------------------------

