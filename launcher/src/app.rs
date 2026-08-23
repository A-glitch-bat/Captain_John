//--------------------------------

// Imports
use softbuffer::{Context, Surface};
use std::{
    io,
    thread,
    rc::Rc,
    sync::mpsc,
    process::{Child, Command},
    path::{Path, PathBuf},
};
use std::os::windows::process::CommandExt;
use winit::{
    application::ApplicationHandler,
    dpi::{LogicalSize, PhysicalPosition},
    event::{ElementState, MouseButton, WindowEvent},
    event_loop::{ActiveEventLoop, ControlFlow},
    window::{Window, WindowId, WindowLevel},
};

use crate::status::Status;
use crate::ui::bubble::draw_bubble;
use crate::ui::panel::draw_panel;
//--------------------------------

const BUBBLE_SIZE: u32 = 96;
const PANEL_WIDTH: u32 = 320;
const PANEL_HEIGHT: u32 = 220;

enum WorkerMessage {
    FrontendStarted(Child),
    Error(String),
    BackendOnline,
    BackendOffline(String),
}

#[derive(Clone, Copy)]
enum LauncherMode {
    Bubble,
    Panel,
}

#[derive(Clone, Copy)]
enum LauncherButton {
    Close,
    Frontend,
    Backend,
    Cyberspace,
}

#[derive(Clone, Copy)]
struct ButtonBounds {
    x: u32,
    y: u32,
    width: u32,
    height: u32,
}

impl ButtonBounds {
    const fn new(x: u32, y: u32, width: u32, height: u32) -> Self {
        Self {
            x,
            y,
            width,
            height,
        }
    }

    fn contains(self, x: f64, y: f64) -> bool {
        x >= self.x as f64
            && x < (self.x + self.width) as f64
            && y >= self.y as f64
            && y < (self.y + self.height) as f64
    }
}

fn panel_button_at(x: f64, y: f64, width: u32) -> Option<LauncherButton> {
    let buttons = [
        (LauncherButton::Close, ButtonBounds::new(0, 0, 32, 32)),
        (
            LauncherButton::Frontend,
            ButtonBounds::new(width.saturating_sub(56), 62, 34, 34),
        ),
        (
            LauncherButton::Backend,
            ButtonBounds::new(width.saturating_sub(56), 106, 34, 34),
        ),
        (
            LauncherButton::Cyberspace,
            ButtonBounds::new(16, 158, width.saturating_sub(32), 34),
        ),
    ];

    buttons
        .iter()
        .find(|(_, bounds)| bounds.contains(x, y))
        .map(|(button, _)| *button)
}

pub struct FrontLauncher {
    pub frontend_status: Status,
    pub backend_status: Status,
    worker_rx: Option<mpsc::Receiver<WorkerMessage>>,
    frontend_process: Option<Child>,
    backend_rx: Option<mpsc::Receiver<WorkerMessage>>,
    window: Option<Rc<Window>>,
    surface: Option<Surface<Rc<Window>, Rc<Window>>>,
    mode: LauncherMode,
    cursor_position: Option<(f64, f64)>,
}

impl Default for FrontLauncher {
    fn default() -> Self {
        Self {
            frontend_status: Status::Offline,
            backend_status: Status::Offline,
            worker_rx: None,
            frontend_process: None,
            backend_rx: None,
            window: None,
            surface: None,
            mode: LauncherMode::Bubble,
            cursor_position: None,
        }
    }
}

// find main file regardless of run location
fn find_app_root(exe_path: &Path) -> io::Result<PathBuf> {
    let exe_dir = exe_path.parent().ok_or_else(|| {
        io::Error::new(
            io::ErrorKind::NotFound,
            "Could not determine the launcher directory",
        )
    })?;

    for directory in exe_dir.ancestors() {
        if directory.join("main.py").is_file() {
            return Ok(directory.to_path_buf());
        }
    }

    Err(io::Error::new(
        io::ErrorKind::NotFound,
        format!("Could not find main.py above {}", exe_dir.display()),
    ))
}

impl FrontLauncher {
    fn start_frontend_service(&mut self) {
        println!("Starting frontend");
        self.frontend_status = Status::Starting;

        if let Some(window) = self.window.as_ref() {
            window.request_redraw();
            println!("Button turned yellow!");
        }

        let (tx, rx) = mpsc::channel();
        self.worker_rx = Some(rx);
     
        thread::spawn(move || {
            let result = std::env::current_exe()
                .and_then(|exe_path| find_app_root(&exe_path))
                .and_then(|app_root| {
                    let main_path = app_root.join("main.py");

                    Command::new("py")
                        .args(["-3.11"])
                        .arg(&main_path)
                        .current_dir(&app_root)
                        .env("JOHN_LAUNCHER", "1")
                        .creation_flags(0x08000000)
                        .spawn()
                        .map_err(|error| {
                            io::Error::new(
                                error.kind(),
                                format!(
                                    "Failed to run pyw -3.11 \"{}\" from \"{}\": {}",
                                    main_path.display(),
                                    app_root.display(),
                                    error
                                ),
                            )
                        })
                });

            let message = match result {
                Ok(child) => WorkerMessage::FrontendStarted(child),
                Err(error) => WorkerMessage::Error(format!("Could not launch main.py: {}", error)),
            };

            let _ = tx.send(message);
        });
    }

    fn stop_frontend_service(&mut self) {
        println!("Stopping frontend");

        if let Some(mut process) = self.frontend_process.take() {
            if let Err(error) = process.kill() {
                eprintln!("Could not stop frontend process: {error}");
            }

            let _ = process.wait();
        }

        self.frontend_status = Status::Offline;

        if let Some(window) = self.window.as_ref() {
            window.request_redraw();
        }
    }
    

    fn start_backend_service(&mut self) {
        println!("Checking backend health");
        self.backend_status = Status::Starting;

        if let Some(window) = self.window.as_ref() {
            window.request_redraw();
        }

        let (tx, rx) = mpsc::channel();
        self.backend_rx = Some(rx);

        thread::spawn(move || {
            let result = reqwest::blocking::get("http://localhost:8080/health")
                .and_then(|response| response.error_for_status())
                .and_then(|response| response.json::<serde_json::Value>());

            let message = match result {
                Ok(body)
                    if body.get("status").and_then(|value| value.as_str()) == Some("healthy") =>
                {
                    WorkerMessage::BackendOnline
                }
                Ok(body) => WorkerMessage::BackendOffline(format!(
                    "Unexpected health response: {body}"
                )),
                Err(error) => WorkerMessage::BackendOffline(error.to_string()),
            };

            let _ = tx.send(message);
        });

    }

    fn check_backend_messages(&mut self) {
        let message = self.backend_rx.as_ref().and_then(|rx| rx.try_recv().ok());

        match message {
            Some(WorkerMessage::BackendOnline) => {
                self.backend_status = Status::Online;
                self.backend_rx = None;
            }
            Some(WorkerMessage::BackendOffline(error)) => {
                eprintln!("Backend health check failed: {error}");
                self.backend_status = Status::Offline;
                self.backend_rx = None;
            }
            Some(_) | None => return,
        }

        if let Some(window) = self.window.as_ref() {
            window.request_redraw();
        }
    }

    fn check_worker_messages(&mut self) {
        let message = self.worker_rx.as_ref().and_then(|rx| rx.try_recv().ok());

        match message {
            Some(WorkerMessage::FrontendStarted(child)) => {
                println!("Worker succeeded.");
                self.frontend_process = Some(child);
                self.frontend_status = Status::Online;
                self.worker_rx = None;
            }

            Some(WorkerMessage::Error(error)) => {
                eprintln!("Worker failed: {error}");
                self.frontend_status = Status::Offline;
                self.worker_rx = None;
            }

            Some(WorkerMessage::BackendOnline) | Some(WorkerMessage::BackendOffline(_)) => return,

            None => return,
        }

        if let Some(window) = self.window.as_ref() {
            window.request_redraw();
        }
    }

    fn check_frontend_process(&mut self) {
        let Some(process) = self.frontend_process.as_mut() else {
            return;
        };

        match process.try_wait() {
            Ok(None) => {}
            Ok(Some(status)) => {
                println!("Frontend exited with status: {status}");
                self.frontend_process = None;
                self.frontend_status = Status::Offline;

                if let Some(window) = self.window.as_ref() {
                    window.request_redraw();
                }
            }
            Err(error) => {
                eprintln!("Could not check frontend process: {error}");
                self.frontend_process = None;
                self.frontend_status = Status::Offline;

                if let Some(window) = self.window.as_ref() {
                    window.request_redraw();
                }
            }
        }
    }

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
//--------------------------------

impl ApplicationHandler for FrontLauncher {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.window.is_some() {
            return;
        }

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

        if let Some(monitor) = window.current_monitor() {
            let monitor_position = monitor.position();
            let monitor_size = monitor.size();

            let margin = 120;
            let x = monitor_position.x + monitor_size.width as i32 - BUBBLE_SIZE as i32 - margin;
            let y = monitor_position.y + monitor_size.height as i32 - BUBBLE_SIZE as i32 - margin;
            window.set_outer_position(PhysicalPosition::new(x, y));
        }

        let context = Context::new(window.clone()).unwrap();
        let surface = Surface::new(&context, window.clone()).unwrap();

        self.window = Some(window);
        self.surface = Some(surface);
        self.start_backend_service();
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
                    if let Some((x, y)) = self.cursor_position {
                        match panel_button_at(x, y, window.inner_size().width) {
                            Some(LauncherButton::Close) => {
                                event_loop.exit();
                            }

                            Some(LauncherButton::Frontend) => {
                                println!("Frontend button clicked");

                                match self.frontend_status {
                                    Status::Offline => self.start_frontend_service(),
                                    Status::Online => self.stop_frontend_service(),
                                    Status::Starting => {}
                                }

                                if let Some(window) = self.window.as_ref() {
                                    window.request_redraw();
                                }
                            }

                            Some(LauncherButton::Backend) => {
                                println!("Backend button clicked");

                                if self.backend_status != Status::Starting {
                                    self.start_backend_service();
                                }

                                if let Some(window) = self.window.as_ref() {
                                    window.request_redraw();
                                }
                            }

                            Some(LauncherButton::Cyberspace) => {
                                println!("Cyberspace button clicked");
                            }

                            None => {}
                        }
                    }
                    else {
                        println!("Black space clicked");
                    }
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
                        let _ =
                            window.request_inner_size(LogicalSize::new(PANEL_WIDTH, PANEL_HEIGHT));

                        self.position_panel_from_bubble();
                    }

                    LauncherMode::Panel => {
                        let panel_pos = window.outer_position().ok();

                        self.mode = LauncherMode::Bubble;

                        let _ =
                            window.request_inner_size(LogicalSize::new(BUBBLE_SIZE, BUBBLE_SIZE));

                        if let Some(pos) = panel_pos {
                            let bubble_x = pos.x + PANEL_WIDTH as i32 - BUBBLE_SIZE as i32;
                            let bubble_y = pos.y + PANEL_HEIGHT as i32 - BUBBLE_SIZE as i32;

                            window.set_outer_position(PhysicalPosition::new(bubble_x, bubble_y));
                        }
                    }
                }

                window.request_redraw();
            }

            WindowEvent::CursorMoved { position, .. } => {
                self.cursor_position = Some((position.x, position.y));
            }

            WindowEvent::RedrawRequested => {
                if let Some(surface) = self.surface.as_mut() {
                    match self.mode {
                        LauncherMode::Bubble => draw_bubble(window, surface),
                        LauncherMode::Panel => draw_panel(window, surface, &self.frontend_status, &self.backend_status),
                    }
                }
            }
            _ => {}
        }
    }

    fn about_to_wait(&mut self, event_loop: &ActiveEventLoop) {
        self.check_worker_messages();
        self.check_frontend_process();
        self.check_backend_messages();

        if self.worker_rx.is_some() || self.backend_rx.is_some() {
            event_loop.set_control_flow(ControlFlow::Poll);
        } else {
            event_loop.set_control_flow(ControlFlow::Wait);
        }
    }
}
//--------------------------------

