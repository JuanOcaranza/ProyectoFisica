import { writeFileSync, readFileSync } from "fs";

export function readDB() {
    return JSON.parse(readFileSync('db/database.json', "utf-8"));
}

export function writeDB(data) {
    writeFileSync('db/database.json', JSON.stringify(data, null, 2), "utf-8");
}