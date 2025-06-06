list_of_items {  } #comment

list_of_items { first_value,
                second_value,
                third_value,
                subsequent,
                and_subsequent,
                and_finally_the_last } #comment

list_of_items { first_value          = 0x01,
                second_value         = 0x02,
                third_value          = 0x04,
                subsequent           = 0x08,
                and_subsequent       = 0x10,
                and_finally_the_last = 0x20 } #comment

list_of_items : first_value
              , second_value
              , third_value
              , subsequent
              , and_subsequent
              , and_finally_the_last

multiline := first_value,         second_value,        third_value,
             subsequent,          and_subsequent,      and_finally_the_last # multiline

const unsigned first_value          = 0x01;
const unsigned second_value         = 0x02;
const unsigned third_value          = 0x04;
const unsigned subsequent           = 0x08;
const unsigned and_subsequent       = 0x10;
const unsigned and_finally_the_last = 0x20;
