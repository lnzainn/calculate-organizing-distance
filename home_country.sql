CREATE TABLE organized_a_competition
AS (SELECT DISTINCT(wca_id)
    FROM competition_organizers co
JOIN users u ON co.organizer_id = u.id AND wca_id IS NOT NULL);

----------------------------------------------------------------

CREATE TABLE mostFrequentCountry AS
WITH RankedCountries AS (
  SELECT
    r.person_id,
    c.country_id,
    COUNT(*) AS appearances,
    ROW_NUMBER() OVER (PARTITION BY r.person_id ORDER BY COUNT(*) DESC) AS rn
  FROM results r
  JOIN competitions c ON r.competition_id = c.id
  WHERE r.person_id IN (
    SELECT wca_id
    FROM persons
    WHERE sub_id = 1
      AND wca_id IN (SELECT wca_id FROM organized_a_competition)
  )
  GROUP BY r.person_id, c.country_id
)
SELECT
  person_id,
  country_id AS mostFrequentCountry
FROM RankedCountries
WHERE rn = 1;
 
# This creates the table for storing most frequent country of all the competitors who have organized atleast one competition

----------------------------------------------------------------

SELECT x.wca_id, x.competition_id, x.competition_country, mf.mostFrequentCountry AS home_country
FROM (SELECT wca_id, competition_id, country_id AS competition_country
      FROM competition_organizers co
JOIN users u ON co.organizer_id = u.id 
JOIN competitions c ON co.competition_id = c.id) x

JOIN mostfrequentcountry mf ON x.wca_id = mf.person_id
