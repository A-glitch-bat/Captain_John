use std::{num::NonZeroU32, rc::Rc};
use softbuffer::{Context, Surface};
use winit::{
    application::ApplicationHandler,
    dpi::LogicalSize,
    event::{ElementState, MouseButton, WindowEvent},
    event_loop::{ActiveEventLoop, ControlFlow, EventLoop},
    window::{Window, WindowId, WindowLevel},
};

const TIME: f32 = 0.0;
const SIZE: u32 = 96;
const CYAN: [u8; 3] = [0, 255, 255];
const PINK: [u8; 3] = [255, 105, 180];

struct FrontLauncher {
    window: Option<Rc<Window>>,
    surface: Option<Surface<Rc<Window>, Rc<Window>>>,
}

impl Default for FrontLauncher {
    fn default() -> Self {
        Self {
            window: None,
            surface: None,
        }
    }
}

impl ApplicationHandler for FrontLauncher {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        let window = Rc::new(
            event_loop
                .create_window(
                    Window::default_attributes()
                        .with_title("Captain John")
                        .with_inner_size(LogicalSize::new(SIZE, SIZE))
                        .with_resizable(false)
                        .with_decorations(false)
                        .with_transparent(true)
                        .with_window_level(WindowLevel::AlwaysOnTop),
                )
                .unwrap(),
        );

        let context = Context::new(window.clone()).unwrap();
        let surface = Surface::new(&context, window.clone()).unwrap();

        self.window = Some(window);
        self.surface = Some(surface);
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _window_id: WindowId,
        event: WindowEvent,
    ) {
        let Some(window) = self.window.as_ref() else {
            return;
        };

        match event {
            WindowEvent::CloseRequested => event_loop.exit(),

            WindowEvent::MouseInput {
                state: ElementState::Pressed,
                button: MouseButton::Left,
                ..
            } => {
                let _ = window.drag_window();
            }

            WindowEvent::MouseInput {
                state: ElementState::Pressed,
                button: MouseButton::Right,
                ..
            } => {
                event_loop.exit();
            }

            WindowEvent::RedrawRequested => {
                if let Some(surface) = self.surface.as_mut() {
                    draw_popup(window, surface);
                }
            }

            _ => {}
        }
    }

    fn about_to_wait(&mut self, _event_loop: &ActiveEventLoop) {
        if let Some(window) = self.window.as_ref() {
            window.request_redraw();
        }
    }
}


fn main() {
    let event_loop = EventLoop::new().unwrap();
    event_loop.set_control_flow(ControlFlow::Wait);

    let mut app = FrontLauncher::default();

    event_loop.run_app(&mut app).unwrap();
}


fn draw_popup(window: &Window, surface: &mut Surface<Rc<Window>, Rc<Window>>) {
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


fn rgba(r: u8, g: u8, b: u8, a: u8) -> u32 {
    ((a as u32) << 24) | ((r as u32) << 16) | ((g as u32) << 8) | b as u32
}

fn blending_to_rgba(coeficient: f32, mute_factor: f32, alpha: u8) -> u32 {
    let thr = coeficient.clamp(0.0, 1.0);
    let m = mute_factor.clamp(0.0, 1.0);
    let [cr, cg, cb] = CYAN;
    let [pr, pg, pb] = PINK;

    let r = (1.0 - thr) * cr as f32 + thr * pr as f32;
    let g = (1.0 - thr) * cg as f32 + thr * pg as f32;
    let b = (1.0 - thr) * cb as f32 + thr * pb as f32;

    rgba((r * m) as u8, (g * m) as u8, (b * m) as u8, alpha)
}
