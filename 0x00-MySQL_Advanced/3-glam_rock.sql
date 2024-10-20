-- SQL script to list Glam rock bands ranked by their longevity
SELECT
    band_name,
    IFNULL(2022 - formed, 0) - IFNULL(2022 - IFNULL(split, 2022), 0) AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%'
ORDER BY
    lifespan DESC;