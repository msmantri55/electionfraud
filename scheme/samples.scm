;; Various election scenarios pulled from Wikipedia pages

(define abc-election-choose-2
  (append
   (make-list 30 '(andrew brian))
   (make-list 6 '(andrew catherine))
   (make-list 9 '(brian andrew))
   (make-list 7 '(brian catherine))
   (make-list 28 '(catherine brian))
   (make-list 20 '(catherine andrew))))

(define abcd-election-choose-3
  (append
   (make-list 34 '(andrea brad carter))
   (make-list 17 '(brad carter andrea))
   (make-list 22 '(carter brad andrea))
   (make-list 10 '(carter delilah brad))
   (make-list 37 '(delilah carter brad))))

(define abcd-election-choose-4
  (append
   (make-list 51 '(andrew catherine brian david))
   (make-list 5 '(catherine brian david andrew))
   (make-list 23 '(brian catherine david andrew))
   (make-list 21 '(david catherine brian andrew))))

(define tennessee-capital-election
  (append
   (make-list 42 '(memphis nashville chattanooga knoxville))
   (make-list 26 '(nashville chattanooga knoxville memphis))
   (make-list 15 '(chattanooga knoxville nashville memphis))
   (make-list 17 '(knoxville chattanooga nashville memphis))))
