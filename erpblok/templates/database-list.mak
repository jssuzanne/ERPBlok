<label for="databases">Select the database to drop</label>
<select id="database">
    % for db in databases:
        <option value="${db}">${db}</option> \
    % endfor
</select>
