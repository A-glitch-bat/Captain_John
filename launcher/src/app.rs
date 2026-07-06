//--------------------------------

// Imports
use std::rc::Rc;

use softbuffer::{Context, Surface};
use winit::{
    application::ApplicationHandler,
    dpi::{LogicalSize, PhysicalPosition},
    event::{ElementState, MouseButton, WindowEvent},
    event_loop::ActiveEventLoop,
    window::{Window, WindowId, WindowLevel},
};
//--------------------------------


use crate::ui::bubble::draw_bubble;
use crate::ui::panel::draw_panel;
const BUBBLE_SIZE: u32 = 96;
const PANEL_WIDTH: u32 = 320;
const PANEL_HEIGHT: u32 = 220;

#[derive(Clone, Copy)]
enum LauncherMode {
    Bubble,
    Panel,
}

pub struct FrontLauncher {
    window: Option<Rc<Window>>,
    surface: Option<Surface<Rc<Window>, Rc<Window>>>,
    mode: LauncherMode,
}

impl Default for FrontLauncher {
    fn default() -> Self {
        Self {
            window: None,
            surface: None,
            mode: LauncherMode::Bubble,
        }
    }
}

impl FrontLauncher {
    fn position_panel_from_bubble(&self) {
        let Some(window) = self.window.as_ref() else {
            return;
        };

        let Ok(bubble_pos) = window.outer_position() else {
            return;
        };

        let Some(monitor) = window.current_monitor() else {
            return;
        };

        let monitor_pos = monitor.position();
        let monitor_size = monitor.size();

        let screen_left = monitor_pos.x;
        let screen_top = monitor_pos.y;
        let screen_right = monitor_pos.x + monitor_size.width as i32;
        let screen_bottom = monitor_pos.y + monitor_size.height as i32;

        let bubble_x = bubble_pos.x;
        let bubble_y = bubble_pos.y;

        // Default: expand left and up from the bubble.
        let mut panel_x = bubble_x + BUBBLE_SIZE as i32 - PANEL_WIDTH as i32;
        let mut panel_y = bubble_y + BUBBLE_SIZE as i32 - PANEL_HEIGHT as i32;

        // If not enough room on the left, expand right instead.
        if panel_x < screen_left {
            panel_x = bubble_x;
        }

        // If not enough room above, expand downward instead.
        if panel_y < screen_top {
            panel_y = bubble_y;
        }

        // Clamp just in case
        if panel_x + PANEL_WIDTH as i32 > screen_right {
            panel_x = screen_right - PANEL_WIDTH as i32;
        }

        if panel_y + PANEL_HEIGHT as i32 > screen_bottom {
            panel_y = screen_bottom - PANEL_HEIGHT as i32;
        }

        window.set_outer_position(PhysicalPosition::new(panel_x, panel_y));
    }
}

impl ApplicationHandler for FrontLauncher {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        let window = Rc::new(
            event_loop
                .create_window(
                    Window::default_attributes()
                        .with_title("Captain John")
                        .with_inner_size(LogicalSize::new(BUBBLE_SIZE, BUBBLE_SIZE))
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
            } => match self.mode {
                LauncherMode::Bubble => {
                    let _ = window.drag_window();
                }
                LauncherMode::Panel => {
                    // Later: handle panel buttons here.
                }
            },

            WindowEvent::MouseInput {
                state: ElementState::Pressed,
                button: MouseButton::Right,
                ..
            } => {
                match self.mode {
                    LauncherMode::Bubble => {
                        self.mode = LauncherMode::Panel;
                        let _ = window.request_inner_size(LogicalSize::new(
                            PANEL_WIDTH,
                            PANEL_HEIGHT,
                        ));

                        self.position_panel_from_bubble();
                    }

                    LauncherMode::Panel => {
                        let panel_pos = window.outer_position().ok();

                        self.mode = LauncherMode::Bubble;

                        let _ = window.request_inner_size(LogicalSize::new(
                            BUBBLE_SIZE,
                            BUBBLE_SIZE,
                        ));

                        if let Some(pos) = panel_pos {
                            let bubble_x = pos.x + PANEL_WIDTH as i32 - BUBBLE_SIZE as i32;
                            let bubble_y = pos.y + PANEL_HEIGHT as i32 - BUBBLE_SIZE as i32;

                            window.set_outer_position(PhysicalPosition::new(bubble_x, bubble_y));
                        }
                    }
                }

                window.request_redraw();
            }

            WindowEvent::RedrawRequested => {
                if let Some(surface) = self.surface.as_mut() {
                    match self.mode {
                        LauncherMode::Bubble => draw_bubble(window, surface),
                        LauncherMode::Panel => draw_panel(window, surface),
                    }
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

