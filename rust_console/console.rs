use std::io;
use std::process::Command;

fn main() {
    println!(r"
███████╗██╗   ██╗███████╗██████╗ ██╗   ██╗██████╗ ███████╗
██╔════╝██║   ██║██╔════╝██╔══██╗██║   ██║██╔══██╗██╔════╝
███████╗██║   ██║█████╗  ██████╔╝██║   ██║██║  ██║█████╗  
╚════██║██║   ██║██╔══╝  ██╔═══╝ ██║   ██║██║  ██║██╔══╝  
███████║╚██████╔╝███████╗██║     ╚██████╔╝██████╔╝███████╗
╚══════╝ ╚═════╝ ╚══════╝╚═╝      ╚═════╝ ╚═════╝ ╚══════╝
    Welcome to the Cyberpunk Console. Type `help` for commands.
");

    let mut input = String::new();
    loop {
        input.clear();
        print!("> ");
        io::Write::flush(&mut io::stdout()).unwrap(); // Flush stdout for clean prompt display
        io::stdin().read_line(&mut input).expect("Failed to read line");
        let command = input.trim();

        match command {
            "help" => display_help(),
            "stats" => display_stats(),
            "exit" => {
                println!("Shutting down... Goodbye, netrunner.");
                break;
            }
            _ => println!("Unknown command: `{}`. Try `help`.", command),
        }
    }
}

fn display_help() {
    println!(r"
Available Commands:
  help    - Show this help message
  stats   - Display system stats
  exit    - Exit the program
");
}

fn display_stats() {
    println!("Fetching system stats...");

    if cfg!(target_os = "windows") {
        // Use WMIC for Windows
        match Command::new("cmd")
            .args(&["/C", "wmic os get Caption,Version,OSArchitecture"])
            .output()
        {
            Ok(output) => {
                println!(
                    "System Info:\n{}",
                    String::from_utf8_lossy(&output.stdout).trim()
                );
            }
            Err(_) => println!("Unable to fetch system stats. Make sure WMIC is available."),
        }
    } else {
        // Use uname for UNIX systems
        match Command::new("uname").arg("-a").output() {
            Ok(output) => {
                println!("System Info:\n{}", String::from_utf8_lossy(&output.stdout));
            }
            Err(_) => println!("Unable to fetch system stats. Is 'uname' installed?"),
        }
    }
}
