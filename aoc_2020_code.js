// # Christalee Bieber, 2020 # cbieber@alum.mit.edu
//
// # Advent of Code 2020 # http://adventofcode.com/2020/ Utility fns

const fs = require('fs');

const input = function (filename) {
    return fs
        .readFileSync("input_2020/" + filename, 'utf8')
        .split('\n')
        .slice(0, -1);
}

const range = function (start, stop, step = 1) {
    let rng = new Array();
    if (step > 0) {
        for (let i = start; i < stop; i += step) {
            rng.push(i);
        }
    }
    if (step < 0) {
        for (let i = start; i > stop; i += step) {
            rng.push(i);
        }
    }

    return rng;
}

const sum = function (arr) {
    let s = 0;
    for (const elem of arr) {
        s += elem;
    }
    return s;
}

const zip = function (m, n) {
    let zipped = new Array();
    for (let x in m) {
        zipped.push([m[x], n[x],]);
    }
    return zipped;
}

const compare = function (m, n) {
    let same = true;
    for (const x in m) {
        let a = m[x];
        let b = n[x];
        if (a != b) {
            same = false;
        }
    }
    return same;
}

const dedupe = function (arr) {
    let deduped = arr.slice();
    for (const a in arr) {
        for (const b in arr) {
            if (a != b) {
                s = compare(arr[a], arr[b]);
                if (s && b > a) {
                    const i = deduped.indexOf(arr[a]);
                    deduped.splice(i, 1);
                }
            }
        }
    }
    return deduped;
}

const count = function (char, arr) {
    let c = 0;
    for (const elem of arr) {
        if (elem == char) {
            c += 1;
        }
    }
    return c;
}

// Puzzle solutions

const day16 = function (info) {
    if (info === undefined) {
        info = input("day16.txt");
    }

    let mine;
    let tickets = new Array();
    let fields = new Map();

    for (const i in info) {
        const line = info[i];
        if (line.startsWith("your")) {
            mine = info[Number(i) + 1]
                .split(",")
                .map(x => Number(x));
        }
        if (line.startsWith("nearby")) {
            for (j = Number(i) + 1; j < info.length; j++) {
                tickets.push(info[j].split(",").map(x => Number(x)));
            }
        } else {
            if (line.includes("or")) {
                const [k, v,] = line.split(": ");
                fields.set(k, v.split(" or "));
            }
        }
    }

    const parsed = function () {
        for (const h of fields.keys()) {
            let g = new Array();
            for (const f of fields.get(h)) {
                const [a, b,] = f
                    .split("-")
                    .map(x => Number(x));
                g.push(range(a, b + 1));
            }
            fields.set(h, g.flat());
        }
    }
    parsed();

    let error = new Array();
    const valid = function (num) {
        let v = new Array();
        for (const x of fields.values()) {
            if (x.includes(num)) {
                v.push(true);
            }
        }
        return v.includes(true);
    }
    for (const t of tickets) {
        for (const val of t) {
            if (!valid(val)) {
                error.push(val);
            }
        }
    }
    const part1 = sum(error);

    valid_tickets = new Array();
    for (const t of tickets) {
        let v = new Array();
        for (const val of t) {
            v.push(valid(val));
        }
        if (!v.includes(false)) {
            valid_tickets.push(t);
        }
    }
    let ranges = new Array();
    for (const field in mine) {
        ranges[field] = [mine[field]];
    }
    for (const vt of valid_tickets) {
        for (const field in vt) {
            ranges[field].push(vt[field]);
        }
    }

    let field_labels = new Map();
    for (const i in ranges) {
        const r = ranges[i]
        let field_names = new Array();
        for (const k of fields.keys()) {
            let vals = fields.get(k);
            let range_in_field = new Array();
            for (const elem of r) {
                if (!vals.includes(elem)) {
                    range_in_field.push(false);
                }
            }
            if (!range_in_field.includes(false)) {
                field_names.push(k);
            }
        }
        field_labels.set(i, field_names);
    }

    const remove_entries = () => {
        for (const [k, v,] of field_labels.entries()) {
            if (v.length == 1) {
                for (let [l, w,] of field_labels.entries()) {
                    if (l != k) {
                        let i = w.findIndex(elem => elem == v[0]);
                        if (i != -1) {
                            w.splice(i, 1);
                        }
                    }
                }
            }
        }
    }
    for (let k of field_labels.keys()) {
        v = field_labels.get(k);
        while (v.length != 1) {
            remove_entries();
            v = field_labels.get(k);
        }
    }

    let part2 = 1;
    for (const [k, v,] of field_labels.entries()) {
        if (v[0].startsWith("departure")) {
            part2 = part2 * mine[parseInt(k)];
        }
    }

    return [part1, part2,];
}

const day15 = function (seq, iter) {
    if (seq === undefined) {
        seq = [
            6,
            4,
            12,
            1,
            20,
            0,
            16,
        ];
    }

    let indices = new Map();

    for (const i in seq) {
        indices.set(seq[i], [parseInt(i)]);
    }
    let curr = seq.slice(-1)[0];

    for (const x of range(seq.length, iter)) {
        if (x % 10000 == 0) {
            console.log(x);
        }
        let old_is = indices.get(curr);
        if (old_is.length == 1 || old_is == undefined) {
            curr = 0;
        } else {
            curr = old_is[1] - old_is[0];
        }

        let new_is = indices.get(curr);
        if (new_is != undefined) {
            indices.set(curr, [
                new_is.slice(-1)[0],
                x,
            ]);
        } else {
            indices.set(curr, [x]);
        }
    }

    return curr;
}

const day14_part2 = function (ops) {
    if (ops === undefined) {
        ops = input("day14.txt");
    }

    const convert = function (num) {
        const s = new Array(...Number(num).toString(2));
        const f = new Array(36 - s.length).fill("0");
        const g = f.concat(s);
        let r = new Array();
        for (i in mask) {
            if (mask[i] == "1" || mask[i] == "X") {
                r.push(mask[i]);
            } else {
                r.push(g[i]);
            }
        }

        return r;
    }

    const floating = function (arr) {
        const s = arr.join("");
        let addresses = new Array(s);
        while (addresses[0].includes("X")) {
            new_addrs = new Array();
            for (const x of addresses) {
                new_addrs.push(x.replace("X", "0"));
                new_addrs.push(x.replace("X", "1"));
            }
            addresses = new_addrs.slice();
        }
        return addresses;
    }

    let memory = new Map();
    let mask;
    for (const op of ops) {
        let [addr, val,] = op.split(" = ");
        if (addr.startsWith("mask")) {
            mask = new Array(...val);
        }
        if (addr.startsWith("mem")) {
            addr = Number(addr.slice(4, -1));
            for (a of floating(convert(addr))) {
                memory.set(Number(parseInt(a, 2)), Number(val));
            }

        }

    }

    return sum(memory.values());
}

const day14_part1 = function (ops) {
    if (ops === undefined) {
        ops = input("day14.txt");
    }

    const convert = function (num) {
        const s = new Array(...Number(num).toString(2));
        const f = new Array(36 - s.length).fill("0");
        const g = f.concat(s);
        let r = new Array();
        for (i in mask) {
            if (mask[i] == "1" || mask[i] == "0") {
                r.push(mask[i]);
            } else {
                r.push(g[i]);
            }
        }

        return parseInt(r.join(""), 2);
    }

    let memory = new Array();
    let mask;
    for (const op of ops) {
        let [addr, val,] = op.split(" = ");
        if (addr.startsWith("mask")) {
            mask = new Array(...val);
        }
        if (addr.startsWith("mem")) {
            val = convert(Number(val));
            addr = Number(addr.slice(4, -1));
            memory[addr] = val;
        }

    }

    let c = 0;
    for (const elem of memory) {
        if (elem) {
            c += elem;
        }
    }

    return c;
}

const day13_part2 = function (buses) {
    if (buses === undefined) {
        buses = (
            "13,x,x,41,x,x,x,x,x,x,x,x,x,997,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,x,x,x,19,x,x,x," +
            "x,x,x,x,x,x,29,x,619,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17"
        ).split(",");
    }

    let delays = new Map();
    for (const b of buses) {
        if (Number(b)) {
            delays.set(Number(b), Number(buses.indexOf(b)));
        }
    }

    const valid = function (time) {
        let v = true;
        for (const e of delays.keys()) {
            if ((time + delays.get(e)) % e != 0) {
                v = false;
            }
        }
        return v;
    }

    let t = 1000000000000;
    while (t < 2000000000000) {
        if (t % 1000000000 == 0) {
            console.log(t);
        }
        if (valid(t * 13)) {
            console.log(t * 13);
            break;
        }
        t += 1;
    }

    return t * 13;
}

const day13_part1 = function (departure, buses) {
    if (buses === undefined) {
        departure = 1000390;
        buses = (
            "13,x,x,41,x,x,x,x,x,x,x,x,x,997,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,x,x,x,19,x,x,x," +
            "x,x,x,x,x,x,29,x,619,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17"
        ).split(",");
    }

    let times = new Map();
    for (const b of buses) {
        if (Number(b)) {
            const n = Number(b)
            times.set(n * Math.ceil(departure / n) - departure, n);
        }
    }

    const i = Math.min(...times.keys());
    return i * times.get(i);

}

const day12_part2 = function (directions) {
    if (directions === undefined) {
        directions = input("day12.txt");
    }

    const move = function (pos, direction, distance) {
        if (direction == "N") {
            pos[1] += distance;
        }
        if (direction == "E") {
            pos[0] += distance;
        }
        if (direction == "S") {
            pos[1] -= distance;
        }
        if (direction == "W") {
            pos[0] -= distance;
        }
        return pos;
    }

    const rotate = function (direction, degrees) {
        let gap = [
            wp[0] - ship[0],
            wp[1] - ship[1],
        ];
        while (degrees > 0) {
            if (direction == "R") {
                gap = [
                    gap[1], -1 * gap[0],
                ];
            }
            if (direction == "L") {
                gap = [
                    -1 * gap[1],
                    gap[0],
                ];
            }

            wp = [
                ship[0] + gap[0],
                ship[1] + gap[1],
            ];
            degrees -= 90;
        }
    }

    let dir = "E";
    let ship = [0, 0,];
    let wp = [10, 1,];

    for (const d of directions) {
        const c = d[0];
        let n = Number(d.slice(1));

        if (c == "F") {
            while (n > 0) {
                const gap = [
                    wp[0] - ship[0],
                    wp[1] - ship[1],
                ];
                ship = wp.slice();
                wp = [
                    ship[0] + gap[0],
                    ship[1] + gap[1],
                ];
                n -= 1;
            }

        }

        if (["N", "E", "W", "S",].includes(c)) {
            wp = move(wp, c, n);
        }

        if (c == "R" || c == "L") {
            rotate(c, n);
        }
    }

    return Math.abs(ship[0]) + Math.abs(ship[1]);
}

const day12_part1 = function (directions) {
    if (directions === undefined) {
        directions = input("day12.txt");
    }

    const move = function (pos, direction, distance) {
        if (direction == "N") {
            pos[1] += distance;
        }
        if (direction == "E") {
            pos[0] += distance;
        }
        if (direction == "S") {
            pos[1] -= distance;
        }
        if (direction == "W") {
            pos[0] -= distance;
        }
        return pos;
    }

    const dgs = new Map();
    dgs.set("N", 0);
    dgs.set("E", 90);
    dgs.set("S", 180);
    dgs.set("W", 270);

    const turn = function (direction, degrees) {
        const current = dgs.get(dir);
        let next;
        if (direction == "R") {
            next = (current + degrees) % 360;
        }
        if (direction == "L") {
            next = (current - degrees + 360) % 360;
        }
        for (const d of dgs) {
            if (d[1] == next) {
                dir = d[0];
            }
        }
    }

    let dir = "E";
    let ship = [0, 0,];

    for (const d of directions) {
        const c = d[0];
        const n = Number(d.slice(1));

        if (c == "F") {
            ship = move(ship, dir, n);

        }

        if (["N", "E", "W", "S",].includes(c)) {
            ship = move(ship, c, n);
        }

        if (c == "R" || c == "L") {
            turn(c, n);
        }
    }

    return Math.abs(ship[0]) + Math.abs(ship[1]);

}

const day9 = function (xmas) {
    if (xmas === undefined) {
        xmas = input("day9.txt").map(x => Number(x));
    }

    const valid = function (num, rng) {
        let v = false;
        for (const a of rng) {
            for (const b of rng) {
                if (a != b && a + b === num) {
                    v = true;
                }
            }
        }
        return v;
    }

    let p1;
    const hack = function (pre, digits) {
        p = digits.slice(0, pre);

        for (const i in digits.slice(pre)) {
            const d = digits[i];
            const prev = digits.slice(i - pre, i)
            if (!valid(d, prev) && !p.includes(d)) {
                p1 = d;
            }
        }
    }

    hack(25, xmas);

    let n = 2;
    let p2;
    while (n < xmas.length) {
        for (const i in xmas) {
            const rng = xmas.slice(Number(i), Number(i) + n)
            if (sum(rng) === p1) {
                p2 = Math.min(...rng) + Math.max(...rng);
                break;
            }
        }
        n += 1;
    }

    return [p1, p2,];
}

const day8 = function (ops) {
if (ops === undefined) {
    ops = input("day8.txt");
}
let p1;
let p2;

const loop = function (program) {
    let acc = 0;
    let i = 0;
    let visited = new Array();

    while (!visited.includes(i)) {
        if (i == program.length) {
            p2 = acc;
            break;
        }
        visited.push(i);
        const [c, d,] = program[i].split(" ");
        if (c == "acc") {
            acc += Number(d);
            i += 1;
        }
        if (c == "jmp") {
            i += Number(d);
        }

        if (c == "nop") {
            i += 1;
        }
    }
    return acc;
}

let mods = new Array();
for (let i in ops) {
    const c = ops[i];
    let d;
    if (c.startsWith("nop")) {
        d = c.replace("nop", "jmp");
    }
    if (c.startsWith("jmp")) {
        d = c.replace("jmp", "nop");
    }
    let n = ops.slice();
    n[i] = d;
    mods.push(n);
}

p1 = loop(ops);
for (p of mods) {
    loop(p);
}

return [p1, p2,];
}

const day7 = function (rules) {
if (rules === undefined) {
    rules = input("day7.txt");
}

let bags = new Array("shiny gold");

for (const b of bags) {
    for (const r of rules) {
        let [outer, inner,] = r.split(" contain ");
        outer = outer
            .split(" ")
            .slice(0, 2)
            .join(" ");
        if (inner.includes(b) && !bags.includes(outer)) {
            bags.push(outer);
        }
    }
}

const p1 = bags.length - 1;

let parsed = new Map();
for (const rule of rules) {
    let [outer, inner,] = rule.split(" contain ");
    const b = inner.split(", ");
    let items = new Map();
    for (const item of b) {
        const t = item.split(" ");
        if (!isNaN(Number(t[0]))) {
            items.set(t.slice(1, 3).join(" "), Number(t[0]));
        }
    }
    parsed.set(outer.split(" ").slice(0, 2).join(" "), items);
}

const bag_count = function (bag) {
    let sum = 1;
    let inner = parsed.get(bag);
    for (const e of inner.entries()) {
        sum += e[1] * bag_count(e[0]);
    }
    return sum;
}

const p2 = bag_count("shiny gold") - 1;

return [p1, p2,];
}

const day6 = function (groups) {
if (groups === undefined) {
    groups = fs.readFileSync('input_2020/day6.txt', 'utf8');
}

let parsed = [];
for (let p of groups.split("\n\n")) {
    p = p
        .trim()
        .replace(/\n/g, " ")
        .split(" ");
    parsed.push(p);
}

let p1 = 0;
let p2 = 0;
for (const p of parsed) {
    let answers = new Set(p.join(""));
    p1 += answers.size;

    let everyone = new Map();
    for (const k of answers) {
        everyone.set(k, 0);
    }

    let chars = "";
    for (const elem of p) {
        const uniq = new Set(elem);
        for (const v of uniq.values()) {
            chars += v;
        }
    }
    for (const char of chars) {
        everyone.set(char, everyone.get(char) + 1);
    }
    for (const item of everyone.entries()) {
        if (item[1] === p.length) {
            p2 += 1;
        }
    }
}
return [p1, p2,];
}

const day5 = function (passes) {
if (passes === undefined) {
    passes = input("day5.txt");
}
const search = function (char, rng) {
    let seats = new Array();
    const l = rng.length;
    if (char == "F" || char == "L") {
        for (let i = rng[0]; i < rng[0] + l / 2; i++) {
            seats.push(i);
        }
    } else {
        for (let i = rng[l - 1] - l / 2 + 1; i <= rng[l - 1]; i++) {
            seats.push(i);
        }
    }

    return seats;
}

const seat_find = function (bp) {
    let row = new Array();
    for (let i = 0; i < 128; i++) {
        row.push(i);
    }

    for (const char of bp.slice(0, -3)) {
        row = search(char, row);
    }

    let seat = new Array();
    for (let i = 0; i < 8; i++) {
        seat.push(i);
    }

    for (const char of bp.slice(-3)) {
        seat = search(char, seat);
    }

    return row[0] * 8 + seat[0];
}

let seat_ids = new Array();
for (const p of passes) {
    seat_ids.push(seat_find(p));
}
seat_ids = seat_ids.sort((a, b) => a - b);
const p1 = seat_ids.slice(-1);

for (i = 0; i < Math.max(...seat_ids); i++) {
    if (i + Math.min(...seat_ids) != seat_ids[i]) {
        const p2 = i + 40;
        break;
    }
}

return [p1, p2,];
}

// TODO finish debugging day4
const day4 = function (passports) {
if (passports === undefined) {
    passports = fs.readFileSync("input_2020/day4.txt", "utf8");
}

let parsed = [];
for (let p of passports.split("\n\n")) {
    p = p
        .replace(/\n/g, " ")
        .split(" ");
    let ids = new Map();
    for (const f of p) {
        let [k, v,] = f.split(":");
        ids.set(k, v);
    }
    parsed.push(ids);
}

let p1 = 0;
let p2 = 0;
const fields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
];
const hexstring = "abcdef0123456789";
const digits = "0123456789";
const eyecolors = [
    "amb",
    "blu",
    "brn",
    "gry",
    "grn",
    "hzl",
    "oth",
];

for (const p of parsed) {
    let f = new Array();
    for (const k of p.keys()) {
        f.push(k);
    }

    let valid = true;
    for (const field of fields) {
        if (!f.includes(field)) {
            valid = false;
        }
    }
    if (valid) {
        p1 += 1;

        let count = 0;
        if (Number(p.get("byr")) >= 1920 && Number(p.get("byr")) <= 2002) {
            count += 1;
        }
        if (Number(p.get("iyr")) >= 2010 && Number(p.get("iyr")) <= 2020) {
            count += 1;
        }
        if (Number(p.get("eyr")) >= 2020 && Number(p.get("eyr")) <= 2030) {
            count += 1;
        }
        if (p.get('hgt').slice(-2) === "cm" && Number(p.get("hgt").slice(0, -2)) >= 150 && Number(p.get("hgt").slice(0, -2)) <= 193) {
            count += 1;
        }
        if (p.get('hgt').slice(-2) === "in" && Number(p.get("hgt").slice(0, -2)) >= 59 && Number(p.get("hgt").slice(0, -2)) <= 76) {
            count += 1;
        }
        if (p.get("hcl").startsWith("#") && p.get("hcl").length === 7) {
            v = true;
            for (const char of p.get("hcl").slice(1)) {
                if (!hexstring.includes(char)) {
                    v = false;
                }
            }
            if (v) {
                count += 1;
            }
        }
        if (eyecolors.includes(p.get("ecl"))) {
            count += 1;
        }
        if (p.get("pid").length === 9) {
            v = true;
            for (const char of p.get("pid")) {
                if (!digits.includes(char)) {
                    v = false;
                }
            }
            if (v) {
                count += 1;
            }
        }
    }
    if (count === 7) {
        p2 += 1;
    }
}

return [p1, p2,];
}

const day3_part2 = function (trees) {
if (trees === undefined) {
    trees = input("day3.txt");
}

const angles = [
    [
        1, 1,
    ],
    [
        1, 3,
    ],
    [
        1, 5,
    ],
    [
        1, 7,
    ],
    [
        2, 1,
    ],
];
let prod = 1;

for (const a of angles) {
    prod *= day3_part1(trees, a);
}

return prod;
}

const day3_part1 = function (trees, angle) {
if (trees === undefined) {
    trees = input("day3.txt");
}
if (angle === undefined) {
    angle = [1, 3,];
}

let p = [0, 0,];
let path = [];

while (p[0] < (trees.length - angle[0])) {
    p = [
        (p[0] + angle[0]),
        (p[1] + angle[1]) % trees[0].length,
    ];
    path.push(trees[p[0]][p[1]]);
}

let count = 0
for (const char of path) {
    if (char == "#") {
        count += 1;
    }
}

return count;
}

const day2 = function (data) {
if (data === undefined) {
    data = input("day2.txt");
}

let p1 = 0;
let p2 = 0;

for (const row of data) {
    let [policy, pw,] = row.split(': ');
    let [range, char,] = policy.split(' ');
    let [min, max,] = range.split('-');

    pw = String(pw)
    min = Number(min)
    max = Number(max)

    let count = 0;
    for (const c of pw) {
        if (c == char) {
            count += 1;
        }
    }
    if (count >= min && count <= max) {
        p1 += 1;
    }

    let v = false;
    if (pw[min - 1] == char || pw[max - 1] == char) {
        v = true;
    }
    if (pw[min - 1] == char && pw[max - 1] == char) {
        v = false;
    }
    if (v) {
        p2 += 1;
    }
}
return [p1, p2,];
}

const day1 = function (data) {
if (data === undefined) {
    data = input("day1.txt");
}
let p1;
let p2 = 0;

for (const a of data) {
    for (const b of data) {
        if (Number(a) + Number(b) == 2020) {
            p1 = Number(a) * Number(b);
        }
        for (const c of data) {
            if (Number(a) + Number(b) + Number(c) == 2020 && Number(a) * Number(b) * Number(c) > p2) {
                p2 = Number(a) * Number(b) * Number(c);
            }
        }
    }
}

return [p1, p2,];
}
