//--------------------------------

// Imports
use std::rc::Rc;

use softbuffer::{Context, Surface};
use winit::{
    application::ApplicationHandler,
    dpi::LogicalSize,
    event::{ElementState, MouseButton, WindowEvent},
    event_loop::ActiveEventLoop,
    window::{Window, WindowId, WindowLevel},
};
//--------------------------------


use crate::drawing::draw_popup;
const SIZE: u32 = 96;

pub struct FrontLauncher {
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
//--------------------------------

