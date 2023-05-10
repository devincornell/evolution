
use std::time::{Duration, Instant};

use std::cmp::Ordering;
use std::io;
use rand::Rng;


//mod status;
mod status;
mod hexpos;

fn main() {
    let pos = hexpos::new(0, 0, 0);
    println!("{:?}", pos);
}

