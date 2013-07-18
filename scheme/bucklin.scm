;; http://en.wikipedia.org/wiki/Bucklin_voting

(define (bucklin-votes-considered n)
  (if (< n 1) (error 'bucklin-bad-round-number)
      (lambda (x)
	(if (< (length x) n)
	    ()
	    (list-tail (reverse x) (- (length x) n))))))

(define (bucklin-round round votes results)
  (let* ((half (/ (length (irv-not-exhausted votes)) 2))
	 (votes-considered (flatten-once (map (bucklin-votes-considered round) votes)))
	 (thisround (tally (filter notfalse? votes-considered)))
	 (maybewinner (leader thisround))
	 (newresults (cons thisround results)))
    (if (> (cdr maybewinner) half)
	newresults
	(bucklin-round (+ round 1) votes newresults))))
      
(define (bucklin-vote votes)
  (bucklin-round 1 votes ()))

(bucklin-vote tennessee-capital-election)