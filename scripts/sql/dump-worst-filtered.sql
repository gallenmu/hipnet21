create temp view export as

WITH

pre AS (

	select ts, hdr from (
		SELECT ts, hdr, count(1) over (partition by hdr) as c
		FROM pkt
		JOIN capture USING (capture_id)
		WHERE 
			capture.name = :'name'
			AND capture."type" = 'pre'
	) as yolo where c = 1
)

, post AS (
	SELECT ts, hdr
	FROM pkt
	JOIN capture USING (capture_id)
	WHERE 
		capture.name = :'name'
		AND capture."type" = 'post'
)

, match AS (
SELECT
	post.ts - pre.ts as latency,
	pre.ts AS prets,
	post.ts as postts,
	encode(pre.hdr, 'hex')
FROM  pre JOIN  post USING (hdr)
WHERE post.ts > pre.ts
    AND post.ts < pre.ts + 5 * 1e9
)

SELECT *                                                                        
FROM  match                                                                     
WHERE postts > 1000000000 + (SELECT MIN(postts) from match);

\copy (select * from export order by latency desc, prets, postts asc limit 5000) to pstdout csv header
