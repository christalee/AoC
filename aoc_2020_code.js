// # Christalee Bieber, 2020
// # cbieber@alum.mit.edu
//
// # Advent of Code 2020
// # http://adventofcode.com/2020/

// Utility fns

const fs = require('fs');

const input = function (filename) {
  return fs.readFileSync("input_2020/" + filename, 'utf8').split('\n').slice(
    0, -1);
}

const range = function (start, stop, step = 1) {
  let rng = new Array();
  for (let i = start; i < stop; i += step) {
    rng.push(i);
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

// Puzzle solutions

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

  return [p1, p2];
}

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
      const [c, d] = program[i].split(" ");
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

  return [p1, p2];
}

const day6 = function (groups) {
  if (groups === undefined) {
    groups = fs.readFileSync('input_2020/day6.txt', 'utf8');
  }

  let parsed = [];
  for (let p of groups.split("\n\n")) {
    p = p.trim().replace(/\n/g, " ").split(" ");
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
  return [p1, p2];
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

  return [p1, p2];
}

// TODO finish debugging day4
const day4 = function (passports) {
  if (passports === undefined) {
    passports = fs.readFileSync("input_2020/day4.txt", "utf8");
  }

  let parsed = [];
  for (let p of passports.split("\n\n")) {
    p = p.replace(/\n/g, " ").split(" ");
    let ids = new Map();
    for (const f of p) {
      let [k, v] = f.split(":");
      ids.set(k, v);
    }
    parsed.push(ids);
  }

  let p1 = 0;
  let p2 = 0;
  const fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
  const hexstring = "abcdef0123456789";
  const digits = "0123456789";
  const eyecolors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];

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
      if (p.get('hgt').slice(-2) === "cm" && Number(p.get("hgt").slice(0, -2)) >=
        150 && Number(p.get("hgt").slice(0, -2)) <= 193) {
        count += 1;
      }
      if (p.get('hgt').slice(-2) === "in" && Number(p.get("hgt").slice(0, -2)) >=
        59 && Number(p.get("hgt").slice(0, -2)) <= 76) {
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

  return [p1, p2];
}

const day3_part2 = function (trees) {
  if (trees === undefined) {
    trees = input("day3.txt");
  }

  const angles = [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]];
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
    angle = [1, 3];
  }

  let p = [0, 0];
  let path = [];

  while (p[0] < (trees.length - angle[0])) {
    p = [(p[0] + angle[0]), (p[1] + angle[1]) % trees[0].length];
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
    let [policy, pw] = row.split(': ');
    let [range, char] = policy.split(' ');
    let [min, max] = range.split('-');

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
  return [p1, p2];
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
        if (Number(a) + Number(b) + Number(c) == 2020 && Number(a) * Number(b) *
          Number(c) > p2) {
          p2 = Number(a) * Number(b) * Number(c);
        }
      }
    }
  }

  return [p1, p2];
}
