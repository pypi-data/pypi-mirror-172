import numpy as np
from cardinal.utils import ActiveLearningSplitter
from pytest import raises


def test_active_learning_splitter():

    splitter = ActiveLearningSplitter(100)
    y = np.zeros(100)
    y[1] = 1
    y[2] = 2

    splitter.initialize_with_random(4, at_least_one_of_each_class=y)
    assert(np.in1d([1, 2], np.where(splitter.selected)).all())

    assert(splitter.current_iter == 0)
    splitter.add_batch([3, 5, 7])
    assert(splitter.current_iter == 1)
    
    # Test initialization with indices
    splitter = ActiveLearningSplitter(100)
    splitter.initialize_with_indices([0, 13, 42])
    assert(splitter.selected.sum() == 3)
    assert(np.in1d([0, 13, 42], np.where(splitter.selected)[0]).all())

    # Full test using _at functions
    splitter = ActiveLearningSplitter(100)
    with raises(ValueError):
        splitter.selected
    splitter.initialize_with_indices(np.arange(10))
    assert(splitter.selected.sum() == 10)
    assert(splitter.selected_at(0).sum() == 10)
    assert(splitter.non_selected_at(0).sum() == 90)
    assert(splitter.current_iter == 0)
    with raises(ValueError):
        splitter.batch_at(0)
    splitter.add_batch(np.arange(10))
    assert(splitter.selected.sum() == 20)
    assert(splitter.selected_at(0).sum() == 10)
    assert(splitter.selected_at(1).sum() == 20)
    assert(splitter.non_selected_at(0).sum() == 90)
    assert(splitter.non_selected.sum() == 80)
    assert(splitter.current_iter == 1)
    assert((np.logical_or(splitter.selected_at(0), splitter.batch_at(0)) == splitter.selected_at(1)).all())

    y = np.arange(10).repeat(10)
    splitter = ActiveLearningSplitter.train_test_split(100, test_size=.2, stratify=y)
    splitter.initialize_with_random(n_init_samples=10, at_least_one_of_each_class=y[splitter.train])
  
    assert(splitter.selected.sum() == 10)
    assert(splitter.current_iter == 0)


def test_active_learning_splitter_random_init():

    n_samples = 10000
    n_test = 1000
    n_classes = 50
    for i in range(10):
        test_indices = np.random.choice(10000, replace=False, size=n_test)
        splitter = ActiveLearningSplitter(n_samples, test_index=test_indices)
        classes = np.random.choice(n_classes, replace=True, size=n_samples)
        splitter.initialize_with_random(n_classes, classes[splitter.train])
        assert(np.unique(classes[splitter.selected]).shape[0] == n_classes)