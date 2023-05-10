
mod hexcoord;

fn main() {
    let pos = hexcoord::HexCoord::new(0, 0, 0);
    println!("{:?}", pos);
}
