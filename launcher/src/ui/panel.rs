//--------------------------------

// Imports
use std::{num::NonZeroU32, rc::Rc};

use softbuffer::Surface;
use winit::window::Window;
//--------------------------------


use crate::colors::rgba;

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
            buffer[(y * width + x) as usize] = rgba(20, 25, 40, 230);
        }
    }

    buffer.present().unwrap();
}
//--------------------------------

