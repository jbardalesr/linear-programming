function minimun_ratio_test(col:: Vector{Float64}, b:: Vector{Float64})
    r_min = 1
    min_val = Inf
    for k=1:size(b, 1)
        if col[k] > 0
            min_val_temp = b[k]/col[k]
            if min_val > min_val_temp
                min_val = min_val_temp
                r_min = k
            end
        end
    end
    return r_min
end

function pivoting(tableau:: Matrix{Float64}, row:: Int64, col:: Int64)
    tableau[row, :] = tableau[row, :]/tableau[row, col]
    for k=1:size(tableau, 1)
        if k != row
            tableau[k, :] = tableau[k, :] - tableau[k, col]*tableau[row, :]
        end
    end
    return tableau
end

function simplex(tableau:: Matrix{Float64}, basic_var:: Matrix{Int64})
    show(stdout, "text/plain", tableau)
    while any(tableau[1, :] .> 0)
        # max criterion
        c_max = argmax(tableau[1, 1:end - 1])
        # minimum ratio test
        r_min = minimun_ratio_test(tableau[2:end, c_max], tableau[2:end, end]) + 1
        # pivoting
        tableau = pivoting(tableau, r_min, c_max)
        # swap row with col
        basic_var[r_min - 1] = c_max
        show(stdout, "text/plain", tableau)
    end
end

tableau = [3 2 0 0 0 0 0.;
           1 1 1 0 0 0 9.;
           3 1 0 1 0 0 18;
           1 0 0 0 1 0 7.;
           0 1 0 0 0 1 6.]

basic_var = [2 3 4 5]
simplex(tableau, basic_var);
