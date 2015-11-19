# -*- coding: utf-8 -*-
from couchdb.design import ViewDefinition

PLAN_FIELDS = ['planID']
PLAN_CHANGES_FIELDS = PLAN_FIELDS + [
    'dateModified',
]


def add_index_options(doc):
    doc['options'] = {'local_seq': True}


def sync_design_plan(db):
    views = [j for i, j in globals().items() if "_planview" in i]
    ViewDefinition.sync_many(db, views, callback=add_index_options)
    plans_count_view.sync(db)


# count
count_map = 'function(doc) { emit(doc.procuringEntity.identifier.id, 1); }'
count_reduce = 'function(keys, values) { return sum(values); }'
plans_count_view = ViewDefinition('plans',
                                  'count_plans',
                                  count_map,
                                  reduce_fun=count_reduce)

plans_all_planview = ViewDefinition('plans', 'all', '''function(doc) {
    if(doc.doc_type == 'Plan' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % PLAN_CHANGES_FIELDS)

plans_by_dateModified_planview = ViewDefinition('plans', 'by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Plan') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % PLAN_FIELDS)

plans_real_by_dateModified_planview = ViewDefinition('plans', 'real_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Plan' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % PLAN_FIELDS)

plans_test_by_dateModified_planview = ViewDefinition('plans', 'test_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Plan' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % PLAN_FIELDS)

plans_by_local_seq_planview = ViewDefinition('plans', 'by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Plan') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % PLAN_CHANGES_FIELDS)

plans_real_by_local_seq_planview = ViewDefinition('plans', 'real_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Plan' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % PLAN_CHANGES_FIELDS)

plans_test_by_local_seq_planview = ViewDefinition('plans', 'test_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Plan' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % PLAN_CHANGES_FIELDS)
