//--------------------------------

// Imports
mod app;
mod colors;
mod drawing;

use app::FrontLauncher;
use winit::event_loop::{ControlFlow, EventLoop};
//--------------------------------


fn main() {
    let event_loop = EventLoop::new().unwrap();
    event_loop.set_control_flow(ControlFlow::Wait);

    let mut app = FrontLauncher::default();

    event_loop.run_app(&mut app).unwrap();
}
//--------------------------------

