export const preprocessingTechniques = [
    {
        name: "Remove NAN values",
        value: "Remove NAN values",
        parameters: [
            {
                name: "axis",
                type: "select",
                options: [0, 1],
                default: 0,
                render: true,
                optional: true,
            },
            {
                name: "how",
                type: "select",
                options: ["any", "all"],
                default: "any",
                render: true,
                optional: true,
            },
            {
                name: "subset",
                type: "columnList",
                render: true,
                optional: true,
            },
            {
                name: "inplace",
                type: "bool",
                options: [true, false],
                default: false,
                render: true,
                optional: true,
            },
          ],
    },
    {
        //add iterative imputer

        name: "Replace NAN values",
        value: "Replace NAN values",
        parameters: [
          {
            name: "column",
            type: "columnName",   
            render: true,
            optional: false,
          },
          {
            name: "missing_values",
            type: "any",    //int | float | str | np.nan| None |pandas.NA
            default: 'np.nan',
            render: true,
            optional: true,
          },
          {
            name: "strategy",
            type: "select",
            options: ['mean','median','most_frequent','constant'],
            default: 'mean',
            render: true,
            optional: false,
          },
          {
            name: "fill_value",  //for 'constant' strategy
            type: "str | number",
            default: 'None',
            render: true,
            optional: true, //check
          },
        ],
    },
    {
        name: "Dropping rows or columns",
        value: "Dropping rows or columns",
        parameters: [
          {
            name: "labels",
            type: "columnList",   
            render: true,
            optional: false,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1],
            defaultValue: 1,
            render: true,
            optional: true,
          },
          {
            name: "inplace",
            type: "bool",
            options: [true, false],
            defaultValue: false,
            render: true,
            optional: true,
          },
          {
            name: "errors",
            type: "select",
            options: ["ignore", "raise"],
            defaultValue: "raise",
            render: true,
            optional: true,
          },
        ],
    },
    {
        name: "Remove Outliers",
        value: "Remove Outliers",
        parameters: [
          {
            name: "columns",
            type: "columnList",
            render: true,
            optional: false,
          },
        ],
    },
    {
        name: "Drop Duplicates",
        value: "Drop Duplicates",
        parameters: [
          {
            name: "subset",
            type: "columnList",   
            render: true,
            optional: true,
          },
          {
            name: "keep",
            type: "select",
            options: ['first','last', false],
            default: 'first',
            render: true,
            optional: true,
          },
          {
            name: "inplace",
            type: "bool",
            options: [true, false],
            defaultValue: false,
            render: true,
            optional: true,
          },
          {
            name: "ignore_index",
            type: "bool",
            options: [true, false],
            defaultValue: false,
            render: true,
            optional: true,
          },
        ],
    },
    {
        name: "Change Data Type",
        value: "Change Data Type",
        parameters: [
          {
            name: "column",
            type: "columnName",
            render: true,
            optional: false,
          },
          {
            name: "data type",
            type: "string",
            render: true,
            optional: false,
          },
          {
            name: "copy",
            type: "bool",
            options: [true, false],
            defaultValue: true,
            render: true,
            optional: true,
          },
          {
            name: "errors",
            type: "select",
            options: ['raise', 'ignore'],
            defaultValue: 'raise',
            render: true,
            optional: true,
          },
        ],
    },
    {
        name: "Round Data",
        value: "Round Data",
        parameters: [
          {
            name: "decimals",
            type: "dict",
            render: true,
            optional: false,
          },
        ],
    },
    {
        name: "Filter DataFrame",
        value: "Filter DataFrame",
        parameters: [
          {
            name: "items",
            type: "list",
            render: true,
            optional: true,  //check
          },
          {
            name: "like",
            type: "string",
            render: true,
            optional: true, //check
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1, 'None'],
            default: 'None',
            render: true,
            optional: true, //check
          },
        ],
    },
    {
        name: "Truncate DataFrame",
        value: "Truncate DataFrame",
        parameters: [
          {
            name: "before",
            type: "any",  //date | str | int (column name or index)
            render: true,
            optional: false,
          },
          {
            name: "after",
            type: "any",  //date | str | int (column name or index)
            render: true,
            optional: false,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1, 'None'],
            default: 'None',
            render: true,
            optional: false,
          },
          {
            name: "copy",
            type: "bool",
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          }
        ],
    },
    {
        name: "Sort Values",
        value: "Sort Values",
        parameters: [
          {
            name: "by",
            type: "columnList",  
            render: true,
            optional: false,
          },
          {
            name: "ascending",
            type: "select", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1],
            default: 0,
            render: true,
            optional: true,
          },
          {
            name: "inplace",
            type: "bool",
            options: [true, false],
            default: false,
            render: true,
            optional: true,
          },
          {
            name: "kind",
            type: "select",
            options: ["quicksort", "mergesort", "heapsort", "stable"],
            default: "quicksort",
            render: true,
            optional: true,
          },
          {
            name: "na_position",
            type: "select",
            options: ["first", "last"],
            default: "last",
            render: true,
            optional: true,
          },
          {
            name: "ignore_index",
            type: "bool",
            options: [true, false],
            default: false,
            render: true,
            optional: true,
          },          
        ],
    },
    {
        name: "Transpose DataFrame",
        value: "Transpose DataFrame",
    },
    {
        name: "Min Max Scaler",
        value: "Min Max Scaler",
        parameters: [
          {
            name: "columns",
            type: "columnList", 
            render: true,
            optional: false,
          },
          {
            name: "feature_range",
            type: "tuple", //(min,max)
            default: '(0, 1)', 
            render: true,
            optional: true,
          },
          {
            name: "copy",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "clip",
            type: "bool", 
            options: [true, false],
            default: false,
            render: true,
            optional: true,
          },
        ],
    },
    {
        name: "Max Abs Scaler",
        value: "Max Abs Scaler",
        parameters: [
          {
            name: "columns",
            type: "columnList", 
            render: true,
            optional: false,
          },
          {
            name: "copy",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          
        ],
    },
    {
        name: "Robust Scaler",
        value: "Robust Scaler",
        parameters: [
          {
            name: "column",
            type: "columnName", 
            render: true,
            optional: false,
          },
          {
            name: "with_centering",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "with_scaling",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "copy",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "unit_variance",
            type: "bool", 
            options: [true, false],
            default: false,
            render: true,
            optional: true,
          },
          {
            name: "quantile_range",
            type: "tuple", 
            default: '(25.0,75.0)',
            render: true,
            optional: true,
          },
        ],
    },
    {
        name: "Standard Scaler",
        value: "Standard Scaler",
        parameters: [
          {
            name: "column",
            type: "columnName", 
            render: true,
            optional: false,
          },
          {
            name: "copy",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "with_mean",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "with_std",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          
        ],
    },
    {
        name: "Normalization",
        value: "Normalization",
        parameters: [
          {
            name: "column",
            type: "columnName", 
            render: true,
            optional: false,
          },
          {
            name: "norm",
            type: "select", 
            options: ['l1','l2','max'],
            default: "l2",
            render: true,
            optional: true,
          },
          {
            name: "copy",
            type: "bool", 
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },

        ],
    },
    {
        name: "Ordinal Encoding",
        value: "Ordinal Encoding",
        parameters: [
          {
            name: "columns",
            type: "columnList",   
            render: true,
            optional: false,
          },
          {
            name: "categories",
            type: "list", //or auto  
            default: 'auto',
            render: true,
            optional: true,
          },
          {
            name: "dtype",
            type: "str", 
            default: "np.float64",
            render: true,
            optional: true,
          },
          {
            name: "handle_unknown",
            type: "select", 
            options: ['error', 'use_encoded_value'],
            default: 'error',
            render: true,
            optional: true,
          },
          {
            name: "unknown_value",  //for 'use_encoded_value'
            type: "int", //int | np.nan 
            default: 'None',
            render: true,
            optional: true,
          },
          {
            name: "encoded_missing_value",  
            type: "int", //int | np.nan 
            default: 'np.nan',
            render: true,
            optional: true,
          },
        ],
    },
    {
        name: "One Hot Encoding",
        value: "One Hot Encoding",
        parameters: [
          {
            name: "columns",
            type: "columnList",   
            render: true,
            optional: false,
          },
          {
            name: "categories",
            type: "list", //or auto  
            default: 'auto',
            render: true,
            optional: true,
          },
          {
            name: "dtype",
            type: "str", 
            default: "np.float",
            render: true,
            optional: true,
          },
          {
            name: "handle_unknown",
            type: "select", 
            options: ['error', 'ignore','infrequent_if_exist'],
            default: 'error',
            render: true,
            optional: true,
          },
          {
            name: "sparse",  
            type: "bool",
            options: [true, false],
            default: true,
            render: true,
            optional: true,
          },
          {
            name: "min_frequency",  
            type: "float",
            default: 'None',
            render: true,
            optional: true,
          },
          {
            name: "max_categories",  
            type: "integer",
            default: 'None',
            render: true,
            optional: true,
          },
        ],
    },
]
