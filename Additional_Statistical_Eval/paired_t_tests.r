library(ggplot2)  
library(dplyr)
library(reshape2)  # For melt function

# Set the root directory
root_dir <- "../Results/SDM"

# Function to recursively find all CSV files
find_csv_files <- function(directory) {
  file_list <- list.files(directory, recursive = TRUE, full.names = TRUE)
  csv_files <- file_list[grepl(".csv$", file_list) & !grepl("(gender.csv$|race.csv$|religion.csv$)", file_list)]
  return(csv_files)
}

# Get all CSV files
csv_files <- find_csv_files(root_dir)

# Read each CSV file and save their names
file_names <- c()
# Initialize algorithm_means as NULL
algorithm_means <- NULL
algorithm_random_significance <- NULL
algorithm_pop_significance <- NULL



# Loop through each CSV file
for (file in csv_files) {
  
  # Read the CSV file
  data <- read.csv(file)

  # Get the file name
  file_name <- basename(file)
  # Split the file name at "_"
  file_name <- strsplit(file_name, "\\.")[[1]]
  file_name_parts <- strsplit(file_name, "_")[[1]]

  # Extract the relevant parts from the file name
  dataset <- file_name_parts[1]
  SDM <- file_name_parts[2]
  stereotype <- file_name_parts[3]
  metric <- file_name_parts[4]    
  
  if (dataset == "Goodreads") {
      num_comparisons <- 78
          # Filter the columns by column name userID and AMF
    filtered_data <- data[, c("UserID", "Random", "MostPop", 
                              "ItemKNN", "UserKNN",
                               "BPRMF",
                              "FunkSVD", "MF", "PMF", "PureSVD",
                              "Slim", "DeepFM", "NeuMF",
                              "MultiVAE")]
    } else if (dataset == "ML-children") {
      num_comparisons <- 91
          # Filter the columns by column name userID and AMF
    filtered_data <- data[, c("UserID", "Random", "MostPop", 
                              "ItemKNN", "UserKNN",
                              "VSM", "BPRMF",
                              "FunkSVD", "MF", "PMF", "PureSVD",
                              "Slim", "DeepFM", "NeuMF",
                              "MultiVAE")]
    }


    # Compute the mean for each algorithm
    means <- colMeans(filtered_data[, -1])  # Exclude UserID column

    # Convert means to strings with 3 decimals
    means <- formatC(means, format = "f", digits = 3)

      # Compute t-tests between each algorithm
    algorithms <- colnames(filtered_data)[-1]  # Exclude UserID column
    num_algorithms <- length(algorithms)
    
    # Initialize matrix to store t-test results
    p_test_results <- matrix(NA, nrow = num_algorithms, ncol = num_algorithms,
                            dimnames = list(algorithms, algorithms))

    
    # Perform t-tests and handle cases with low variability
    for (i in 1:num_algorithms) {
      for (j in 1:num_algorithms) {
        if (i != j) {  # Exclude comparisons with the same algorithm
          # Check variability
          if (length(unique(filtered_data[[algorithms[i]]])) > 1 && length(unique(filtered_data[[algorithms[j]]])) > 1) {
            # If variability is sufficient, perform t-test
            t_result <- t.test(filtered_data[[algorithms[i]]], filtered_data[[algorithms[j]]])
            p_test_results[i, j] <- p.adjust(t_result$p.value, method = "bonferroni", n = num_comparisons)

          } else {
            # If variability is not sufficient, assign NA
            p_test_results[i, j] <- NA
          }
        }
      }
    }
    p_test_results <- round(p_test_results, digits = 3)
    p_test_results <- ifelse(p_test_results < 0.05, 0, 1)

    # Add the "VSM" column and row back
    if (dataset == "Goodreads") {
      # Add the "VSM" column
      filtered_data$CB <- 0
      
      # Reorder columns to put "VSM" in its original position
      filtered_data <- filtered_data[, c("UserID", "Random", "MostPop",
                                        "ItemKNN", "UserKNN",
                                        "CB", "BPRMF",
                                        "FunkSVD", "MF", "PMF", "PureSVD",
                                        "Slim", "DeepFM", "NeuMF",
                                        "MultiVAE")]
      
      row_of_zeros <- rep(NA, ncol(p_test_results))
      # Add the "VSM" row
      p_test_results <- rbind(p_test_results[1:4, ], row_of_zeros, p_test_results[5:nrow(p_test_results), ])
      
      
      column_of_zeros <- rep(NA, nrow(p_test_results))
      # Add the "VSM" column
      p_test_results <- cbind(p_test_results[, 1:4], column_of_zeros, p_test_results[,5:ncol(p_test_results)])
      
    }
    rownames(p_test_results)[5] <- "CB"
    colnames(p_test_results)[5] <- "CB"

    melted_p_values <- melt(p_test_results)

all_values_same <- function(x) {
  all(na.omit(x)) && length(unique(na.omit(x))) == 1
}
all_values_same <- all_values_same(melted_p_values$value)

heatmap <- ggplot(melted_p_values, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile(color = "grey90") +  # Add border color
  geom_hline(yintercept = seq(0.5, num_algorithms + 0.5, by = 1), color = "grey50", size = 0.2) +  # Add horizontal grid lines
  geom_vline(xintercept = seq(0.5, num_algorithms + 0.5, by = 1), color = "grey50", size = 0.2) +  # Add vertical grid lines
  scale_fill_gradient(low = if( all_values_same) "#0006c1" else "#af0000", 
                      high = if( all_values_same) "#0006c1" else "#0006c1",
                      na.value = "white") +  # Set the same color if all values are the same
  labs(x = NULL, y = NULL) +
  theme_minimal() +
 
  theme(axis.text.x = element_blank(),  # Remove x-axis labels 
                axis.text.y = element_blank(),  # Increase font size of y-axis labels
                legend.position = "none",  # Remove legend
        )  + 
  # theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 12),  # Rotate x-axis labels and increase font size
  #       axis.text.y = element_text(size = 12),  # Increase font size of y-axis labels
  #       legend.position = "none",  # Remove legend
  #       plot.background = element_rect(fill = "white")) +  # Set background color to white
  coord_fixed()

  

  
if (dataset == "ML-children") {
  dataset <- "ML"
  }

file_path <- paste0("../plots/", dataset, "_", SDM, "_", stereotype, "_", metric, "_p_values_heatmap.png")
# Save the plot
print(file_path)
if (!((dataset == "ML") && (SDM == "biasmeter" || SDM == "lexicon-model") && 
(stereotype == "gender") && (metric == "HITS")))
{
ggsave(file_path, plot = heatmap, width = 8, height = 8, units = "in", dpi = 300)
}  
}
