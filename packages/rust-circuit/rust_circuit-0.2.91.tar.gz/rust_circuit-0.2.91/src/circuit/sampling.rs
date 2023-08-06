use super::{module_nodes::replace_expand_bottom_up, CircResult, CircuitRc, DiscreteVar};

pub fn discrete_var_sample_all<F>(circuit: CircuitRc, should_sample: F) -> CircResult
where
    F: Fn(&DiscreteVar) -> bool,
{
    replace_expand_bottom_up(circuit, |c| {
        if c.as_discrete_var()
            .map(|x| should_sample(x))
            .unwrap_or(false)
        {
            Some(c.as_discrete_var().unwrap().values.clone())
        } else {
            None
        }
    })
}
