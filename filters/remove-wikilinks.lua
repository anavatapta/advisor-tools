-- Remove Obsidian wikilinks [[text]] -> text
-- Also handles [[link|display]] -> display

function Str(el)
  local text = el.text
  
  -- Handle [[link|display]] format first
  text = text:gsub("%[%[([^|%]]+)|([^%]]+)%]%]", "%2")
  
  -- Handle [[text]] format
  text = text:gsub("%[%[([^%]]+)%]%]", "%1")
  
  if text ~= el.text then
    return pandoc.Str(text)
  end
  
  return el
end

function Para(para)
  local new_content = {}
  for i, el in ipairs(para.content) do
    if el.t == "Str" then
      local text = el.text
      -- Handle [[link|display]]
      text = text:gsub("%[%[([^|%]]+)|([^%]]+)%]%]", "%2")
      -- Handle [[text]]
      text = text:gsub("%[%[([^%]]+)%]%]", "%1")
      table.insert(new_content, pandoc.Str(text))
    else
      table.insert(new_content, el)
    end
  end
  return pandoc.Para(new_content)
end
