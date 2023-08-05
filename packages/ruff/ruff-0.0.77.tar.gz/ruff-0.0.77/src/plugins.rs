pub use assert_false::assert_false;
pub use assert_tuple::assert_tuple;
pub use deprecated_unittest_alias::deprecated_unittest_alias;
pub use duplicate_exceptions::duplicate_exceptions;
pub use if_tuple::if_tuple;
pub use invalid_print_syntax::invalid_print_syntax;
pub use print_call::print_call;
pub use super_call_with_parameters::super_call_with_parameters;
pub use type_of_primitive::type_of_primitive;
pub use unnecessary_abspath::unnecessary_abspath;
pub use use_pep585_annotation::use_pep585_annotation;
pub use use_pep604_annotation::use_pep604_annotation;
pub use useless_metaclass_type::useless_metaclass_type;
pub use useless_object_inheritance::useless_object_inheritance;

mod assert_false;
mod assert_tuple;
mod deprecated_unittest_alias;
mod duplicate_exceptions;
mod if_tuple;
mod invalid_print_syntax;
mod print_call;
mod super_call_with_parameters;
mod type_of_primitive;
mod unnecessary_abspath;
mod use_pep585_annotation;
mod use_pep604_annotation;
mod useless_metaclass_type;
mod useless_object_inheritance;
