
use super::ids::{StatusID};
use super::statusrecord::StatusRecord;
use std::vec::Vec;

#[derive(Debug)]
pub struct Status {
    pub id: StatusID,
    pub records: Vec<StatusRecord>,
}

//xs: &[A]


impl Status {
    pub fn from_records(self, records: Vec<StatusRecord>) -> Result<Status, i32> {

        if records.len() == 0 {
            return Err(10)
        }

        for sr in records.iter() {
            if sr.id != records[0].id {
                return Err(10)
            }
        }
        self.from_records_nocheck(records)
    }

    pub fn from_records_nocheck(self, records: Vec<StatusRecord>) -> Result<Status, i32> {
        Ok(Status {
            id: records[0].id,
            records: records,
        })
    }

    pub fn new(id: StatusID) -> Status {
        Status {
            id,
            records: std::vec::Vec::new(),
        }
    }

}

