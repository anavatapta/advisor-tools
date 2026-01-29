-- Convert task list items to regular bullets

function BulletList(el)
  for i, item in ipairs(el.content) do
    -- Check if first element is a plain/para with checkbox
    if item[1] and (item[1].t == "Plain" or item[1].t == "Para") then
      local first = item[1].content[1]
      if first and first.t == "Str" then
        -- Remove [ ] or [x] checkboxes
        local text = first.text
        text = text:gsub("^%[%s*%]%s*", "")
        text = text:gsub("^%[x%]%s*", "")
        text = text:gsub("^%[X%]%s*", "")
        first.text = text
      end
    end
  end
  return el
end
