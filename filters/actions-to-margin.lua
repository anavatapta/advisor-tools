-- Move Actions section to margin notes for Tufte style

local in_actions = false
local actions_items = {}

function Header(el)
  local header_text = pandoc.utils.stringify(el.content):lower()
  
  if el.level == 3 and header_text:match("action") then
    in_actions = true
    return {}  -- Remove the Actions header
  elseif in_actions and el.level <= 3 then
    -- Exit actions section when we hit another header
    in_actions = false
  end
  
  return el
end

function BulletList(el)
  if in_actions then
    -- Build LaTeX for margin note
    local items = {}
    for _, item in ipairs(el.content) do
      local item_text = {}
      for _, block in ipairs(item) do
        if block.t == "Plain" or block.t == "Para" then
          for _, inline in ipairs(block.content) do
            if inline.t == "Str" then
              -- Remove checkbox markers
              local text = inline.text:gsub("^%[%s*%]%s*", ""):gsub("^%[x%]%s*", ""):gsub("^%[X%]%s*", "")
              if text ~= "" then
                table.insert(item_text, text)
              end
            elseif inline.t == "Space" then
              table.insert(item_text, " ")
            end
          end
        end
      end
      if #item_text > 0 then
        table.insert(items, table.concat(item_text))
      end
    end
    
    in_actions = false
    
    -- Create margin note with bullet points
    local latex = "\\marginpar{\\raggedright\\small\\textbf{Actions}\\\\[0.5em]\\begin{itemize}[leftmargin=*,nosep,itemsep=0.3em]"
    for _, item in ipairs(items) do
      latex = latex .. "\\item " .. item
    end
    latex = latex .. "\\end{itemize}}"
    
    return pandoc.RawBlock("latex", latex)
  end
  
  return el
end

return {
  {Header = Header},
  {BulletList = BulletList}
}
