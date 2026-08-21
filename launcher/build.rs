fn main() {
    if cfg!(target_os = "windows") {
        let mut res = winresource::WindowsResource::new();
        res.set_icon("assets/launcher.ico");
        res.compile().unwrap();
    }
}
