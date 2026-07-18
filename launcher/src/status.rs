//--------------------------------

// Imports
use std::fmt;

use crate::colors::rgba;
//--------------------------------


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Offline,
    Starting,
    Online,
}

impl Status {
    pub fn color(&self) -> u32 {
        match self {
            Status::Offline => rgba(200, 50, 50, 255),
            Status::Starting => rgba(220, 180, 40, 255),
            Status::Online => rgba(60, 180, 75, 255),
        }
    }
}

impl fmt::Display for Status {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Status::Offline => write!(f, "Offline"),
            Status::Starting => write!(f, "Starting"),
            Status::Online => write!(f, "Online"),
        }
    }
}
//--------------------------------

