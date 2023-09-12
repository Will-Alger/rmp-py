
CREATE TABLE Teachers (
    typename TEXT,
    avgDifficulty REAL,
    avgRating REAL,
    department TEXT,
    firstName TEXT,
    id TEXT PRIMARY KEY,
    isSaved BOOLEAN,
    lastName TEXT,
    legacyId INTEGER,
    numRatings INTEGER,
    schoolId TEXT,
    schoolName TEXT,
    wouldTakeAgainPercent REAL
);
