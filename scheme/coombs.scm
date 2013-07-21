;; http://en.wikipedia.org/wiki/Coombs%27_method

(define (coombs-last-choice vote)
  (if (irv-exhausted? vote) #f (last vote)))

(define (coombs-round votes results)
  (let* ((half (/ (length (irv-not-exhausted votes)) 2))
	 (first-place (tally 
		       (filter notfalse? 
			       (map irv-first-choice votes))))
	 (last-place (tally
		      (filter notfalse? 
			      (map coombs-last-choice votes))))
	 (maybewinner (leader first-place))
	 (maybeloser (leader last-place)))
    (if (> (cdr maybewinner) half)
	(cons
	 (list first-place last-place)
	 results)
	(coombs-round
	 (irv-disqualify (car maybeloser) votes)
	 (cons
	  (list first-place last-place)
	  results)))))
  
(define (coombs votes)
  (coombs-round votes ()))
  
(coombs tennessee-capital-election)