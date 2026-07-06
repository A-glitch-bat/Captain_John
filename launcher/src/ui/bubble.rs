//--------------------------------

// Imports
use std::{num::NonZeroU32, rc::Rc};

use softbuffer::Surface;
use winit::window::Window;
//--------------------------------


use crate::colors::{blending_to_rgba, rgba};

const TIME: f32 = 0.0;

pub fn draw_bubble(window: &Window, surface: &mut Surface<Rc<Window>, Rc<Window>>) {
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

    let center_x = width as f32 / 2.0;
    let center_y = height as f32 / 2.0;
    let radius = width.min(height) as f32 * 0.39;

    for y in 0..height {
        for x in 0..width {
            let dx: f32 = x as f32 - center_x;
            let dy: f32 = y as f32 - center_y;
            let distance: f32 = (dx * dx + dy * dy).sqrt();

            let pixel: u32 = if distance <= radius {
                blending_to_rgba(0.5, 0.5, 125) // inside the main circle
            } else {
                let angle: f32 = dy.atan2(dx) + TIME;
                //print!("{} ", angle);
                let blend_coefficient = (angle.cos() + 1.0) / 2.0;
                
                if distance <= radius + 3.0{
                    blending_to_rgba(blend_coefficient, 1.0, 255) // bright inner border
                } else if distance <= radius + 6.0 {
                    blending_to_rgba(blend_coefficient, 0.25, 125) // fadeout border
                } else if distance <= radius + 10.0 {
                    blending_to_rgba(blend_coefficient, 0.5, 255) // dull outer glow
                } else {
                    rgba(0, 0, 0, 0) // outside the circle
                }
            };

            buffer[(y * width + x) as usize] = pixel;
        }
    }

    buffer.present().unwrap();
}
//--------------------------------

