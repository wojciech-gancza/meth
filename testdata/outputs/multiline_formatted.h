list_of_items {  } #comment

list_of_items { first_value,
                second_value,
                third_value,
                subsequent,
                and_subsequent,
                and_finally_the_last } #comment

list_of_items : first_value
              , second_value
              , third_value
              , subsequent
              , and_subsequent
              , and_finally_the_last

multiline := first_value,         second_value,        third_value,
             subsequent,          and_subsequent,      and_finally_the_last # multiline
