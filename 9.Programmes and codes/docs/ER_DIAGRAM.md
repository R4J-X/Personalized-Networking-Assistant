# Entity-Relationship Model (Reference Design)

This document describes the normalized relational schema the project is designed to migrate to if/when the JSON-file storage (`data/history.json`, `data/feedback.json`) is replaced with a real database. It is **not** currently implemented in code — the MVP uses flat-file JSON persistence for simplicity (see `app/services/history_logger.py` and `app/services/feedback_logger.py`).

## Entities

| Entity | Primary Key |
|---|---|
| User Profile | `UserID` |
| Event Context | `EventID` |
| Networking Session | `SessionID` |
| Generated Starter | `StarterID` |
| Wikipedia Fact Check | `FactCheckID` |
| Log Entry | `LogID` |

## Relationships

- **User Profile → Networking Session**: 1 to Many. One user can participate in multiple networking sessions.
- **Event Context → Networking Session**: 1 to Many. A single event context can be associated with multiple networking sessions.
- **Networking Session → Generated Starter**: 1 to Many. A single session can yield multiple AI-generated conversation starters.
- **Networking Session → Wikipedia Fact Check**: 1 to Many. A single session can involve multiple fact-checking queries.
- **Networking Session → Log Entry**: 1 to Many. A single session can generate multiple system log entries for auditing.

## Foreign Keys

- `Networking Session` references `User Profile` via `UserID` and `Event Context` via `EventID`.
- `Generated Starter` references `Networking Session` via `SessionID`.
- `Wikipedia Fact Check` references `Networking Session` via `SessionID`.
- `Log Entry` optionally references `Networking Session` via `SessionID`.

## Attributes

**User Profile**
- `UserID` (PK)
- `BioText`
- `currentEventCache`

**Event Context**
- `EventID` (PK)
- `EventDescription`
- `AnalyzedThemes`

**Networking Session**
- `SessionID` (PK)
- `UserID` (FK)
- `EventID` (FK)
- `SessionTimestamp`

**Generated Starter**
- `StarterID` (PK)
- `SessionID` (FK)
- `StarterText`
- `ContextPromptUsed`

**Wikipedia Fact Check**
- `FactCheckID` (PK)
- `SessionID` (FK)
- `VerifiedQueryText`
- `VerificationStatus`
- `WikipediaSourceURL`

**Log Entry**
- `LogID` (PK)
- `SessionID` (FK)
- `ActionType`
- `PayloadJSON`
- `Timestamp`

## Normalization

Data for users, event contexts, core session transactions, AI outputs, and system logs are stored in separate entities, reducing redundancy and ensuring clear traceability of data and AI interactions.

## Use Case Coverage

This model supports:
- Tracking persistent user biographies and mapping them to dynamic event descriptions
- Recording and tracking individual AI-generated conversation prompts per session
- Logging Wikipedia verification queries to ensure factual reliability
- Detailed interaction logging for system auditing, analytics, and performance debugging
