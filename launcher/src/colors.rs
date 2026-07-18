//--------------------------------

pub const CYAN: [u8; 3] = [0, 255, 255];
pub const PINK: [u8; 3] = [255, 105, 180];
//--------------------------------


pub fn rgba(r: u8, g: u8, b: u8, a: u8) -> u32 {
    ((a as u32) << 24) | ((r as u32) << 16) | ((g as u32) << 8) | b as u32
}

pub fn blending_to_rgba(coefficient: f32, mute_factor: f32, alpha: u8) -> u32 {
    let t = coefficient.clamp(0.0, 1.0);
    let m = mute_factor.clamp(0.0, 1.0);

    let [cr, cg, cb] = CYAN;
    let [pr, pg, pb] = PINK;

    let r = (1.0 - t) * cr as f32 + t * pr as f32;
    let g = (1.0 - t) * cg as f32 + t * pg as f32;
    let b = (1.0 - t) * cb as f32 + t * pb as f32;

    rgba((r * m) as u8, (g * m) as u8, (b * m) as u8, alpha)
}

pub fn lighten(color: u32, amount: u8, new_a: u8) -> u32 {
    let r = ((color >> 16) & 0xFF) as u8;
    let g = ((color >> 8) & 0xFF) as u8;
    let b = (color & 0xFF) as u8;

    rgba(
        r.saturating_add(amount),
        g.saturating_add(amount),
        b.saturating_add(amount),
        new_a,
    )
}

pub fn darken(color: u32, amount: u8, new_a: u8) -> u32 {
    let r = ((color >> 16) & 0xFF) as u8;
    let g = ((color >> 8) & 0xFF) as u8;
    let b = (color & 0xFF) as u8;

    rgba(
        r.saturating_sub(amount),
        g.saturating_sub(amount),
        b.saturating_sub(amount),
        new_a,
    )
}
//--------------------------------

