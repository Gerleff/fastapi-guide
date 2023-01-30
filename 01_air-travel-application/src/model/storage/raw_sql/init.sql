CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL,
    role VARCHAR(64) NOT NULL DEFAULT "PASSENGER"
);

CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company INTEGER NOT NULL,
    plane VARCHAR(64) NOT NULL,
    town_from VARCHAR(64) NOT NULL,
    town_to VARCHAR(64) NOT NULL,
    time_out VARCHAR(64) NOT NULL,
    time_in VARCHAR(64) NOT NULL,
    FOREIGN KEY (company)
      REFERENCES companies (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);



CREATE TABLE pass_in_trip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip INTEGER NOT NULL,
    passenger INTEGER NOT NULL,
    place VARCHAR(64) NOT NULL,
    FOREIGN KEY (passenger)
      REFERENCES users (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION,
    FOREIGN KEY (trip)
      REFERENCES trips (id)
         ON DELETE CASCADE
         ON UPDATE NO ACTION
);

INSERT INTO companies (name) VALUES ("AirWonder");
INSERT INTO trips (
    company, plane, town_from, town_to, time_out, time_in
) VALUES (
    1,  "Airbus A220", "Dubai", "Saratov", "2023-01-22T00:48:31.519504", "2023-01-22T03:48:31.519535"
);
INSERT INTO pass_in_trip (trip, passenger, place) VALUES (1, 1, "A21");
INSERT INTO users (name, role) VALUES ("GerGoltz", "ADMIN");
