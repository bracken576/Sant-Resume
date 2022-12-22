(ns correct-change.core
  (:gen-class))
;This program is used to gererate the correct change with the given coins or bills.

(def the_change_is "The change is")

;this method constructs the string representation of the change
(defn printout [coins change_list string_to_print counter]
  (if (== counter 0)
    (if (= (first change_list) 0)
      (recur (rest coins) (rest change_list) the_change_is (inc counter))
      (if (> (first change_list) 1) 
        (recur (rest coins) (rest change_list) (str the_change_is " " (first change_list) " " (key (first coins)) "'s") (inc counter))
        (recur (rest coins) (rest change_list) (str the_change_is " " (first change_list) " " (key (first coins))) (inc counter))))
    (cond
      (= counter 8) (if (= (first change_list) 0)
                      (println string_to_print)
                      (if (not (= (first change_list) nil)) 
                        (println (str string_to_print ", " (first change_list) " " (key (first coins))))
                        (println string_to_print)))
      (= (first change_list) 0) (recur (rest coins) (rest change_list) string_to_print (inc counter))
      (not (= (first change_list) nil)) (if (not(= (count the_change_is) (count string_to_print))) 
                                           (if (> (first change_list) 1) 
                                             (recur (rest coins) (rest change_list) (str string_to_print ", " (first change_list) " " (key (first coins)) "'s") (inc counter)) 
                                             (recur (rest coins) (rest change_list) (str string_to_print ", " (first change_list) " " (key (first coins))) (inc counter))) 
                                           (if (> (first change_list) 1) 
                                             (recur (rest coins) (rest change_list) (str string_to_print " " (first change_list) " " (key (first coins)) "'s") (inc counter))
                                             (recur (rest coins) (rest change_list) (str string_to_print " " (first change_list) " " (key (first coins))) (inc counter))))
      :else (recur (rest coins) (rest change_list) string_to_print (inc counter)))))

(def coinage {"twenty-dollar bill" 2000 "ten-dollar bill" 1000 "five-dollar bill" 500 "dollar bill" 100 "quarter" 25 "dime" 10 "nickel" 5 "penny" 1})

;this method inputs into a list the amount of coins or bills needed per denomination and then calls printout to construct it into a string
(defn -main [coins change_amount change_list]
  (let [new_change_list (conj change_list (int (/ change_amount (val (first coins)))))]
    (if (> (- change_amount (* (first new_change_list) (val (first coins)))) 0)
      (recur (rest coins) (- change_amount (* (first new_change_list) (val (first coins)))) new_change_list)
      (printout coinage (reverse new_change_list) "" 0))))

(-main coinage 2155 nil)