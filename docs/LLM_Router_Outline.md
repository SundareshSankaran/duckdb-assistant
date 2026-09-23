# LLM Router - Outline

The following outlines the approach towards using a Large Language Model (LLM) router that cycles through a list of models (all belonging to the Google Gemini family) to execute tasks requested in a prompt.

## Defining Candidate Models

The `model_list` attribute for every instance of an assistant class (`DuckDBAssistant`) contains candidate models which are available to that instance. This enables differentiation. `model_list` is initially populated bassed on an environmental variable, `FALLBACK_MODELS` and can be subsequently added to, replaced with a new list or pruned further.


```mermaid
graph 

  subgraph Environment

     A[/ FALLBACK_MODELS: gemini-3.8-flash,.. /]
     
     subgraph DuckDBAssistant
        B([Initialise])
        C[self.model_list]
        D[["self.add_models(`model_list: list`)"]]
        E[["self.set_model_list(`model_list: list`)"]]
        F[["self.remove_models(`model_list: list`)"]]

     end

  end

      B --> C
      A -.-> C
      D --> C
      E --> C
      F --> C

```

## Prompt Execution

The user experience from the time of initialising an instance of a `DuckDBAssistant` and then using the instance to generate SQL is depicted below.

```mermaid

sequenceDiagram
    actor User
    participant Init as DuckDBAssistant
    participant model_list as model_list
    participant FB as EnvVar_FALLBACK_MODELS
    participant No_FB as EnvVar_EMPTY

    participant Generate as generate()
    participant IntGenerate as Internal generate method

    User ->> Init: initialises, state(FB,No_FB) 
    Init --> model_list: attribute

    alt state==FB    
        FB -->> model_list: populates 
    else state==No_FB
        No_FB -->> model_list: default of gemini-3.7-flash
    end

    User ->> Init: prompt
    Init ->> Generate: prompt
    model_list ->> Generate: model list
    Generate ->> IntGenerate: prompt, model list

    Note over IntGenerate: cycles through model list
    Note over IntGenerate: calls model in model list until response
    IntGenerate ->> Generate: response
    Generate ->> User: response

```

## Internal Generate Method - Execution

The process followed in the internal generate method (`generate_duckdb_query()`) is depicted below.  The `model_list` is a container of all available candidate models which are accessed based on their position in the list. If a candidate model fails (either due to availability issues emnating from a spike in demand or other reasons), then a time-out is enforced (a random period lasting between 1 - 2 seconds) before the next model in the list is taken up.

```mermaid

flowchart TD
    Start([Start]) --> A
    A[Receive system prompt + user prompt] --> B[LLM Router]
    B --> C[Select next model from model_list]
    C --> D[Call generate_content<br/>with tool configuration]

    D --> E{Request succeeds?}
    E -- Yes --> F[Capture response]
    E -- No --> G[Log error]
    G --> H[Wait random 1–3 seconds]
    H --> I{More models available?}

    I -- Yes --> C
    I -- No --> J[All model attempts failed]

    F --> K[Extract SQL from fenced code block]
    K --> L[Return query + response text]

```