(set-logic BV)

(define-fun origFun ( (X Float) (Y Float) ) Bool 
		(and X Y)
)

(synth-fun skel ( (X Float) (Y Float) ) Bool
		  ((Start Bool (
										  (and Start Start)
										  (or Start Start)
										  (affine X Y)
		  )))
)

(declare-var X Float)
(declare-var Y Float)

(constraint (= (origFun X Y ) (skel X Y)))


(check-synth)
