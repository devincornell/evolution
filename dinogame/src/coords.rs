
use std::cmp::Ordering;
use std::io;
use rand::Rng;


#[derive(Debug)]
struct Coords {
    x: f64,
    y: f64,
}

impl Coords {
    fn normalize(&self) -> Coords {
        let norm = self.norm();
        Coords {
            x: self.x/norm,
            y: self.y/norm,
        }
    }
    fn norm(&self) -> f64{
        ((self.x.powf(2.0)) + (self.y.powf(2.0))).sqrt()
    }
}





fn norm(c: &Coords) -> Coords {
    let m = ((c.x.powf(2.0)) + (c.y.powf(2.0))).sqrt();
    Coords {
        x: c.x/m,
        y: c.y/m,
    }
}

fn main_strings() {
    // https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html
    let mut s = String::from("hello world");
    let l = mylen(&s);
    println!("{}", l);

    add_ending(&mut s);
    let l2 = mylen(&s);
    println!("{}", l2);
    println!("{}", s);
    let end = first_word_end(&s);
    println!("{}", end);

    let c = Coords {x: 1.10, y: -10.3};
    let cn = norm(&c);
    println!("{} {} {} {}", c.x, c.y, cn.x, cn.y);
    println!("{:?}", cn);

    let cn2 = c.normalize();
    println!("{:?}", cn2);

}

fn first_word_end(s: &String) -> usize{
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }
    return s.len()
}

fn add_ending(s: &mut String) {
    s.push_str("homie");
}

fn mylen(s: &String) -> usize {
    s.len()
}


fn main_old2() {
    let mut ct: u32 = 0;
    'cting: loop {
        ct += 1;
        loop {
            ct += 1;
            if ct > 10 {
                break 'cting;
            }
        }
    }
    println!("{}", ct)
}



fn main_old() {
    // left off here: https://doc.rust-lang.org/book/ch03-02-data-types.html
    println!("Guess the number!");
    let secret_number = rand::thread_rng().gen_range(1..=100);
    println!("The secret number is: {secret_number}");

    loop {
        println!("Please input your guess.");
        let mut guess = String::new();
    
        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");
        println!("You guessed: {guess}");
    
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
    
        match guess.cmp(&secret_number) {
            Ordering::Less => println!("too small"),
            Ordering::Greater => println!("too big"),
            Ordering::Equal => {
                println!("right!");
                break;
            },
        }
    }
}







