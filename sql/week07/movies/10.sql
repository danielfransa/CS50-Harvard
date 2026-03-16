-- 10. Names of all directors who have directed a movie that got a rating of at least 9.0
SELECT people.name
FROM people
WHERE people.id IN (
    SELECT directors.person_id
    FROM directors
    JOIN ratings ON directors.movie_id = ratings.movie_id
    WHERE ratings.rating >= 9.0
);