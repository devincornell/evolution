
use std::time::{Duration, Instant};
//mod ids;
use super::ids;


#[derive(Debug)]
pub struct StatusInfo {
    // this object contains info that may not be associated with a tweet
    // if the user has not deleted it

    // most basic info
    pub author_id: ids::UserID,
    pub created_at: Instant,
    pub text: String,

    // relations with other statuses
    pub conversation_id: ids::ConvoID,
    pub quoted: ids::StatusID,
    pub retweeted: ids::StatusID,
    pub replied_to: ids::StatusID,
    pub in_reply_to_user_id: ids::UserID,

    // engagement metrics
    pub retweet_count: u64,
    pub reply_count: u64,
    pub like_count: u64,
    pub quote_count: u64,
    
    // other stuff
    pub source: String, 
    pub lang: String,
    pub possibly_sensitive: String,
}

