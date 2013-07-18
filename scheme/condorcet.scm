;; http://en.wikipedia.org/wiki/Condorcet_method

;; Pairwise counting via matrices requires a complete list of choices to 
;; construct the matrix, in case the individual vote does not include
;; rankings of all choices.

(define (condorcet-matrix vote choices)
  (let ((vote-size (length choices)))
    (make-matrix vote-size vote-size