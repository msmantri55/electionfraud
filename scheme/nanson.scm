;; http://en.wikipedia.org/wiki/Nanson%27s_method

(define (nanson-average results)
  (/ (apply + (map cdr results)) (length results)))

(define (nanson-survivors results)
  (map car
       (filter 
	(lambda (x) (< (cdr x) (nanson-average results)))
	results)))

(define (nanson-filter-one-vote candidates)
  (lambda (vote)
   (filter (lambda (choice) (memq choice vote)) candidates)))

(define (nanson-filter candidates votes)
  (map (nanson-filter-one-vote candidates) votes))

(define (nanson-helper votes previous-rounds)
  (let* ((round-results (borda-one-tally votes))
	 (remaining-candidates (nanson-survivors round-results)))
    (if (= (length remaining-candidates) 1)
	(cons round-results previous-rounds)
	(nanson-helper 
	 (nanson-filter remaining-candidates votes)
	 round-results))))
	 
(define (nanson votes)
  (nanson-helper votes ()))
