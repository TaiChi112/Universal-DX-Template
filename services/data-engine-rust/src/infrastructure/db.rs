use sqlx::postgres::PgPoolOptions;
use sqlx::{Pool, Postgres};
use std::env;
use tokio::time::{sleep, Duration};

/// ฟังก์ชันสำหรับสร้าง Connection Pool
pub async fn establish_connection() -> Pool<Postgres> {
    // ดึง URL ของ Database จาก Environment Variable
    // ตัวอย่าง: postgres://user:password@localhost:5432/universal_dx
    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set in environment");

    // retry เพื่อรองรับช่วงที่ PostgreSQL เพิ่งเริ่มทำงานและยังไม่พร้อมรับการเชื่อมต่อ
    let max_attempts = 20;
    let mut attempt = 1;

    loop {
        match PgPoolOptions::new()
            .max_connections(5)
            .connect(&database_url)
            .await
        {
            Ok(pool) => return pool,
            Err(err) if attempt < max_attempts => {
                eprintln!(
                    "PostgreSQL not ready (attempt {}/{}): {}. Retrying in 2s...",
                    attempt, max_attempts, err
                );
                attempt += 1;
                sleep(Duration::from_secs(2)).await;
            }
            Err(err) => {
                panic!(
                    "Failed to connect to PostgreSQL after {} attempts: {}",
                    max_attempts, err
                );
            }
        }
    }
}

/// สร้างตารางที่จำเป็นหากยังไม่มี เพื่อให้ระบบพร้อมใช้งานทันทีตอนบูต
pub async fn initialize_schema(pool: &Pool<Postgres>) -> Result<(), sqlx::Error> {
    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS documents (
            id BIGSERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            confidence_score DOUBLE PRECISION NOT NULL,
            language TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        "#,
    )
    .execute(pool)
    .await?;

    Ok(())
}