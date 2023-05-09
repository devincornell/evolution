
use std::time::{Duration, Instant};

use std::cmp::Ordering;
use std::io;
use rand::Rng;


//mod status;
mod status;

fn main() {
    let sr = status::StatusRecord::new_empty(
        Instant::now(),
        status::StatusID(String::from("whatevaID")),
        None,
    );
    println!("{:?}", sr);
    let x = status::ConvoInfo {
        id: status::ConvoID(String::from("myid")),
    };
    println!("{:?}", x);
}

