
use std::cmp::Ordering;
use std::io;
use rand::Rng;


#[derive(Debug)]
pub struct HexPos {
    q: i64,
    r: i64,
    s: i64,
}

impl HexPos {
    pub fn new(q: i64, r: i64, s: i64) -> HexPos {
        HexPos{q, r, s}
    }
}











