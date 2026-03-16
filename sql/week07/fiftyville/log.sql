-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT *
FROM crime_scene_reports
WHERE street = "Humphrey Street"
AND year = 2025
AND month = 7
AND day = 28;

-- crime was 10:15am bakery, 3 witnesses

SELECT *
FROM interviews
WHERE year = 2025
AND month = 7
AND day = 28;

-- Ruth, Eugene, Raymond, take money on Leggett Street, into on a car, around 10 min., take the earliest flight out Fiftyville tomarrow 07/29

-- check suspect plates:
SELECT license_plate
FROM bakery_security_logs
WHERE year = 2025
AND month = 7
AND day = 28
AND hour = 10
AND minute >= 15
AND minute <= 25
AND activity = "exit";

-- 5P2BI95 94KL13X 6P58WS2 4328GD8 G412CB7 L93JTIZ 322W7JE 0NTHK55

-- check license_plates

SELECT *
FROM people
WHERE license_plate IN (
    '5P2BI95', '94KL13X', '6P58WS2', '4328GD8',
    'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55'
);

-- suspects list
  --221103|Vanessa|(725) 555-4692|2963008352|5P2BI95
  --243696|Barry|(301) 555-4174|7526138472|6P58WS2
  --396669|Iman|(829) 555-5269|7049073643|L93JTIZ
  --398010|Sofia|(130) 555-0289|1695452385|G412CB7
  --467400|Luca|(389) 555-5198|8496433585|4328GD8
  --514354|Diana|(770) 555-1861|3592750733|322W7JE
  --560886|Kelsey|(499) 555-9472|8294398571|0NTHK55
  --686048|Bruce|(367) 555-5533|5773159633|94KL13X

-- use ATM in Leggett Street - withdraw

SELECT account_number
FROM atm_transactions
WHERE year = 2025
AND month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

-- account_number of transactions ATM:
  --28500762
  --28296815
  --76054385
  --49610011
  --16153065
  --25506511
  --81061156
  --26013199

-- join account_number whit people

SELECT *
FROM people
JOIN bank_accounts
ON people.id = bank_accounts.person_id
WHERE account_number IN (
  '28500762', '28296815', '76054385', '49610011',
  '16153065', '25506511', '81061156', '26013199'
);

-- 2º suspect list:
  --686048|Bruce|(367) 555-5533|5773159633|94KL13X|49610011|686048|2010
  --514354|Diana|(770) 555-1861|3592750733|322W7JE|26013199|514354|2012
  --458378|Brooke|(122) 555-4581|4408372428|QX4YZN3|16153065|458378|2012
  --395717|Kenny|(826) 555-1652|9878712108|30G67EN|28296815|395717|2014
  --396669|Iman|(829) 555-5269|7049073643|L93JTIZ|25506511|396669|2014
  --467400|Luca|(389) 555-5198|8496433585|4328GD8|28500762|467400|2014
  --449774|Taylor|(286) 555-6063|1988161715|1106N58|76054385|449774|2015
  --438727|Benista|(338) 555-6650|9586786673|8X428L0|81061156|438727|2018

-- in 2 lists Bruce, Diana, Iman, Luca

-- short call

SELECT *
FROM phone_calls
WHERE year = 2025
AND month = 7
AND day = 28
AND duration < 60;

-- 221|(130) 555-0289|(996) 555-8899|2025|7|28|51
-- 224|(499) 555-9472|(892) 555-8872|2025|7|28|36
-- 233|(367) 555-5533|(375) 555-8161|2025|7|28|45
-- 251|(499) 555-9472|(717) 555-1342|2025|7|28|50
-- 254|(286) 555-6063|(676) 555-6554|2025|7|28|43
-- 255|(770) 555-1861|(725) 555-3243|2025|7|28|49
-- 261|(031) 555-6622|(910) 555-3251|2025|7|28|38
-- 279|(826) 555-1652|(066) 555-9701|2025|7|28|55
-- 281|(338) 555-6650|(704) 555-2131|2025|7|28|54

-- caller
SELECT name
FROM people
WHERE phone_number IN (
  '(130) 555-0289', '(499) 555-9472', '(367) 555-5533', '(286) 555-6063',
  '(770) 555-1861', '(031) 555-6622', '(826) 555-1652', '(338) 555-6650'
);

-- Kenny Sofia Benista Taylor Diana Kelsey Bruce Carina

-- join caller e receiver is possible that 2 person is in the flight
SELECT
    p1.name AS caller_name,
    pc.caller AS phone_caller,
    p2.name AS receiver_name,
    pc.receiver AS phone_receiver
FROM phone_calls pc
JOIN people p1 ON pc.caller = p1.phone_number
JOIN people p2 ON pc.receiver = p2.phone_number
WHERE pc.year = 2025
  AND pc.month = 7
  AND pc.day = 28
  AND pc.duration < 60;

-- list
  --Sofia|(130) 555-0289|Jack|(996) 555-8899
  --Kelsey|(499) 555-9472|Larry|(892) 555-8872
  --Bruce|(367) 555-5533|Robin|(375) 555-8161
  --Kelsey|(499) 555-9472|Melissa|(717) 555-1342
  --Taylor|(286) 555-6063|James|(676) 555-6554
  --Diana|(770) 555-1861|Philip|(725) 555-3243
  --Carina|(031) 555-6622|Jacqueline|(910) 555-3251
  --Kenny|(826) 555-1652|Doris|(066) 555-9701
  --Benista|(338) 555-6650|Anna|(704) 555-2131

-- tomorrow flight
SELECT *
FROM flights
WHERE year = 2025
AND month = 7
AND day = 29
ORDER BY hour, minute;

-- list of flights
  --36|8|4|2025|7|29|8|20
  --43|8|1|2025|7|29|9|30
  --23|8|11|2025|7|29|12|15
  --53|8|9|2025|7|29|15|20
  --18|8|6|2025|7|29|16|0

-- the earliest flight: 36|8|4|2025|7|29|8|20

-- passagers list:

SELECT pe.passport_number, pe.name
FROM passengers pa
JOIN people pe ON pa.passport_number = pe.passport_number
WHERE flight_id = 36;

-- passager list whit names
  --7214083635|Doris
  --1695452385|Sofia
  --5773159633|Bruce
  --1540955065|Edward
  --8294398571|Kelsey
  --1988161715|Taylor
  --9878712108|Kenny
  --8496433585|Luca

SELECT *
FROM airports
WHERE id = 4


--The THIEF is: Bruce
--The city the thief ESCAPED TO: New York City
--The ACCOMPLICE is: Robin