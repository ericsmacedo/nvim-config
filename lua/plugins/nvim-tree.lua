-- File explorer for neovim
return {
  "nvim-tree/nvim-tree.lua",
  version = "*",
  lazy = false,
  dependencies = {
    "nvim-tree/nvim-web-devicons",
  },

  opts = {
    view = {
      relativenumber = true,
      number = true, -- optional: show absolute line number for current line
    },
  },

  keys = {
    { "<c-n>", "<cmd>NvimTreeToggle<cr>" },
    { "<c-k>", "<c-k>", ft = "fzf", mode = "t", nowait = true },
  },

}
