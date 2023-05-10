
use std::cmp::Ordering;
use std::io;
use rand::Rng;


#[derive(Debug)]
pub struct HexCoord {
    q: i64,
    r: i64,
    s: i64,
}

impl HexCoord {
    pub fn new(q: i64, r: i64, s: i64) -> HexCoord {
        HexCoord{q, r, s}
    }
}











