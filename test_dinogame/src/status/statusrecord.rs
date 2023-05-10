use std::time::{Duration, Instant};
use std::fmt::Display;
use std::io;

//use statusinfo::StatusInfo;
//mod ids;
//mod statusinfo;

use super::ids;
use super::statusinfo;

#[derive(Debug)]
pub struct StatusRecord {
    pub _id: Option<u64>,
    pub request_ts: Instant,
    pub id: ids::StatusID,
    pub added: Option<Instant>,
    pub info: Option<statusinfo::StatusInfo>,
}

impl StatusRecord {
    // probably replace this with constructor created from sql db
    pub fn new(
        _id: Option<u64>,
        request_ts: Instant, 
        id: ids::StatusID,
        added: Option<Instant>,
        author_id: ids::UserID,
        created_at: Instant,
        text: String,
        conversation_id: ids::ConvoID,
        quoted: ids::StatusID,
        retweeted: ids::StatusID,
        replied_to: ids::StatusID,
        in_reply_to_user_id: ids::UserID,
        retweet_count: u64,
        reply_count: u64,
        like_count: u64,
        quote_count: u64,
        source: String, 
        lang: String,
        possibly_sensitive: String,
    ) -> StatusRecord {
            
        StatusRecord {
            _id: None,
            request_ts,
            id,
            added,
            info: Some(statusinfo::StatusInfo {
                author_id,
                created_at,
                text,
                conversation_id,
                quoted,
                retweeted,
                replied_to,
                in_reply_to_user_id,
                retweet_count,
                reply_count,
                like_count,
                quote_count,
                source,
                lang,
                possibly_sensitive,
            }),
        }
    }

    pub fn new_empty(request_ts: Instant, id: ids::StatusID, added: Option<Instant>) -> StatusRecord {
        StatusRecord {
            _id: None,
            request_ts,
            id,
            added,
            info: None,
        }
    }
}


